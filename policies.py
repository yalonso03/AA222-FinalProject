"""
File: policies.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Defines a bunch of different policies that we use in order to try to optimize adaptive streaming.

Each function just takes in the current network bandwidth, the elastic buffer 
"""
import random
import numpy as np
from random import gauss
import NetworkSimulator
import constants


"""
Args for each policy:

    # cur_bandwidth (usually bits/sec)
    # buffer (MB)
    # returns quality (MB/sec)

"""
# Chooses random quality levels and a random server location
def random_policy(cur_bandwidth, num_sec_in_buffer, prev_quality_level, n_rebuffers):
    next_quality_level = random.choice(list(constants.QUALITY_LEVELS.values()))  # choose a random quality level 
    next_loc = random.choice(list(constants.SERVER_EMISSION_GRAMS_PER_MB.keys()))   # choose a random server location
    return next_quality_level, next_loc


def simple_quality_policy(cur_bandwidth, num_sec_in_buffer, prev_quality_level, n_rebuffers):

    """
    
        Simple policy that chooses the maximum quality that will not drain the current buffer
        
        Depending on the throughput, select the highest possible quality rate that the current buffer/bandwidth allows

        We don't care about CO2 for this policy but otherwise, it is intuitively the best current choice. However, it doesn't scale for long horizon problems. 
    
    """

    best_qual = list(constants.QUALITY_LEVELS.values())[0]
    
    for i in range(len(constants.QUALITY_LEVELS)):

        curr_qual = list(constants.QUALITY_LEVELS.values())[i]

        segment_size_MB = curr_qual * constants.N_SECONDS_PER_SEGMENT
        time_to_download_s = segment_size_MB / cur_bandwidth

        # if we can choose this time, choose it (dont think about the future)
        if num_sec_in_buffer >= time_to_download_s:
            best_qual = curr_qual
        else: # otherwise, no other quality will work (we'll have to rebuffer)
            break

    
    next_quality_level = best_qual
    next_loc = random.choice(list(constants.SERVER_EMISSION_GRAMS_PER_MB.keys()))   # choose a random server location
    return next_quality_level, next_loc   


def always_max_quality(cur_bandwidth, num_sec_in_buffer, prev_quality_level, n_rebuffers):
    """
        bad policy: always choose the maximum quality. 
        This could show that we shouldn't always maximize quality -- there will certainly be rebuffers
    """
    next_quality_level = max(list(constants.QUALITY_LEVELS.values())) # choose the maximum quality level each time
    next_loc = random.choice(list(constants.SERVER_EMISSION_GRAMS_PER_MB.keys()))   # choose a random server location
    return next_quality_level, next_loc


def always_min_quality(cur_bandwidth, num_sec_in_buffer, prev_quality_level, n_rebuffers):
    """
        bad policy: always choose the minimum quality. 
        This could show that we shouldn't always minimize quality -- the average quality will be low
        Could provide opportunity for discussion though if a user preference is to have absolutely no jitter, even at the cost of consistently low quality

    """
    next_quality_level = min(list(constants.QUALITY_LEVELS.values())) # choose the minimum quality level each time
    next_loc = random.choice(list(constants.SERVER_EMISSION_GRAMS_PER_MB.keys()))   # choose a random server location
    return next_quality_level, next_loc





"""
using Distributions
function cross_entropy_method(f, P, k_max, m=100, m_elite=10)
    for k in 1 : k_max
        samples = rand(P, m)
        order = sortperm([f(samples[:,i]) for i in 1:m])
        P = fit(typeof(P), samples[:,order[1:m_elite]])
    end
    return P
end



Algorithm 8.8. The cross-entropy
method, which takes an objective
function fto be minimized, a pro-
posal distribution P, an iteration
count k_max, a sample size m, and
the number of samples to use when
refitting the distribution m_elite.
It returns the updated distribution
over where the global minimum is
likely to exist.

"""

# TODO move these into the constants file for cleanness
# all fake constants idk (some are same from textbook)
K_ITER = 5
SAMPLE_SIZE_M = 100
M_ELITE = 3
JITTER_RISK = 2

# then define some weights to use for a scoring method (like weighted for multi objective)
# todo also move this into the constants
w_quality = 0.4
w_rebuffer = 0.3
w_co2 = 0.3

def cross_entropy_policy(cur_bandwidth, num_sec_in_buffer, prev_quality_level, n_rebuffers):

    # we need to have an initial proposal set (like P in the formula)
    # start with all the possible combos since our problem is currently small (might need to change it if we expand server locations + possible quality levels)

    # this will be 6-ish to start out
    candidate_points = []
    for quality in list(constants.QUALITY_LEVELS.values()):
        for loc in list(constants.SERVER_EMISSION_GRAMS_PER_MB.keys()):
            candidate_points.append((quality,loc))

    # start out with uniform probabilities, then all of the weights add to one with the division 
    # this is our proposal distribution (like P in the julia formula)
    prob_weights = np.ones(len(candidate_points)) / len(candidate_points)

    for _ in range(K_ITER):

        # sample candidate indices with current probabilities (this is the "samples = rand(P, m)" line in julia)
        indices = np.random.choice(len(candidate_points), size=SAMPLE_SIZE_M, p=prob_weights)
        sampled = [candidate_points[i] for i in indices] 

        # score each sampled candidate (sorta same as the "sortperm([f(samples[:,i]) for i in 1:m])" line)
        scored = []
        for curr_quality, curr_loc in sampled:

            # figure out possible jitter risk to later put in 
            segment_size_MB = curr_quality * constants.N_SECONDS_PER_SEGMENT
            time_to_download_s = segment_size_MB / cur_bandwidth

            # if we can choose this time, choose it (dont think about the future)
            jitter_risk = 0
            if num_sec_in_buffer < time_to_download_s:
                jitter_risk = JITTER_RISK
            
            # then calculate the score with current jitter risk, CO2, etc
            score = ( # we want the overall score to be minimized 
                -w_quality * curr_quality +         # maximize quality (so we make this negative)
                +w_rebuffer * jitter_risk +         # minimize jitter (so we make this positive)
                +w_co2 * constants.SERVER_EMISSION_GRAMS_PER_MB[curr_loc]  # minimize carbon (so we make this positive)
            )
            scored.append(score)

        # pick elite samples (lowest scores) -- same as the sort perm line.
        # used chat to simplify this idea
        elite_indices = np.argsort(scored)[:M_ELITE] # creates a list of indices that would rank scores from lowest to highest but constrained to the elite samples
        elite_samples = [sampled[i] for i in elite_indices] # then we use the indices to make a list of the scores from there

        # count frequencies of (quality, loc) in elite group
        # this will help with updating the distribution
        # goes over the elite samples and counts how many times each unique (quality, location) pair appears.
        elite_counts = {}
        for quality, loc in elite_samples:

            # get the current count (or 0 if unseen) and increment it (source: chat for simplicity)
            elite_counts[(quality, loc)] = elite_counts.get((quality, loc), 0) + 1 

        # update distribution (aka resetting P) -- normalize frequencies to get new probabilities
        prob_weights = np.zeros(len(candidate_points))

        for idx, candidate in enumerate(candidate_points):

            # first grab the counts for each of the candidate points
            prob_weights[idx] = elite_counts.get(candidate, 0)

        # if all of these counts are zero (they never showed up, then we reset the prob_weights to be what it was at the beginning)
        # todo this might not be needed? added it as a safeguard
        if prob_weights.sum() == 0: 
            prob_weights = np.ones(len(candidate_points)) / len(candidate_points)

        # otherwise we normalize by the existing ones
        else:
            prob_weights /= prob_weights.sum()

    # then we do our final pick: most probable candidate
    best_index = np.argmax(prob_weights) # get the index corresponding to the best score
    best_quality, best_loc = candidate_points[best_index]

    return best_quality, best_loc




# was gonna make it a class at first, this is old, but now i think it makes more sense to just have it be different functions
# class Policy:
#     # Constructor -- will take in the number of segments in the "movie"
#     # policy should be a function that takes in: current bandwidth, current buffer size, etc, and outputs what quality level to pick and where to serve from (TX, CA, WA etc)
#     def __init__(self, cur_network_bandwidth, cur_buffer_size, prev_quality_level, n_rebuffers):
#         self._cur_network_bandwidth = cur_network_bandwidth
#         self._cur_buffer_size = cur_buffer_size
#         self._prev_quality_level = prev_quality_level
#         self.n_rebuffers = n_rebuffers

#     # @kate my idea is that we can have multiple methods here that each take a step per the function. e.g. one for cross entropy, one for a random policy
#     # I'm thinking that we want them to always take in the same parameters (doesn't necessarily need to use the inputted params, but just for consistency)
#     # Then, they should always return consistent decision info: next quality level, location to serve from 
    
#     def cross_entropy_step(self):
#         """ 
#         we can make multiple different policies, one method per policy, then we can run simulations with various policies and compare performance
#         """
#         pass

#     def random_step(self):
#         next_quality_level = random.choice(constants.QUALITY_LEVELS.values())  # choose a random quality level 
#         next_loc = random.choice(constants.LOCATIONS_CO2_DICT.keys())   # choose a random server location
#         return next_quality_level, next_loc

    
    

"""
using Distributions
function cross_entropy_method(f, P, k_max, m=100, m_elite=10)
    for k in 1 : k_max
        samples = rand(P, m)
        order = sortperm([f(samples[:,i]) for i in 1:m])
        P = fit(typeof(P), samples[:,order[1:m_elite]])
    end
    return P
end



Algorithm 8.8. The cross-entropy
method, which takes an objective
function fto be minimized, a pro-
posal distribution P, an iteration
count k_max, a sample size m, and
the number of samples to use when
refitting the distribution m_elite.
It returns the updated distribution
over where the global minimum is
likely to exist.

"""