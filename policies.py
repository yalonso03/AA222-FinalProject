"""
File: policies.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Defines a bunch of different policies that we use in order to try to optimize adaptive streaming.

Each function just takes in the current network bandwidth, the elastic buffer 
"""
import random
from random import gauss
import NetworkSimulator
import constants



def random_policy(cur_bandwidth, buffer, prev_quality_level, _n_rebuffers):
    next_quality_level = random.choice(list(constants.QUALITY_LEVELS.values()))  # choose a random quality level 
    next_loc = random.choice(list(constants.LOCATIONS_CO2_DICT.keys()))   # choose a random server location
    return next_quality_level, next_loc

def cross_entropy_policy(cur_bandwidth, buffer, prev_quality_level, _n_rebuffers):
    pass


# was gonna make it a class at first, this is old, but now i think it makes more sense to just have it be different functions
# class Policy:
#     # Constructor -- will take in the number of segments in the "movie"
#     # policy should be a function that takes in: current bandwidth, current buffer size, etc, and outputs what quality level to pick and where to serve from (TX, CA, WA etc)
#     def __init__(self, cur_network_bandwidth, cur_buffer_size, prev_quality_level, n_rebuffers):
#         self._cur_network_bandwidth = cur_network_bandwidth
#         self._cur_buffer_size = cur_buffer_size
#         self._prev_quality_level = prev_quality_level
#         self._n_rebuffers = n_rebuffers

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

    
        