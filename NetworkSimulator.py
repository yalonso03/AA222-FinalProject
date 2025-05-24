"""
File: NetworkSimulator.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Defines a simulator class for our problem!
"""
from random import gauss
import policy
import constants  # defines constants that are used across multiple files, eg quality levels, server locations, distances from servers etc

# ----------------- CONSTANTS ------------------
#TODO -- check what a realistic value for all of these would be
# Capacity (in Mb) of our buffer
BUFFER_CAPACITY = 100 

# Used to simulate noise at each timestep
NETWORK_THROUGHPUT_MEAN = 50
NETWORK_THROUGHPUT_STD = 10

# ----------------------------------------------


class NetworkSimulator:
    # Constructor -- will take in the number of segments in the "movie"
    # policy should be a function that takes in: current bandwidth, current buffer size, etc, and outputs what quality level to pick and where to serve from (TX, CA, WA etc)
    def __init__(self, n_segments, policy):
        self._cur_time = 0
        self._n_segments = n_segments
        self._policy = policy  # instance of Policy class

        # Randomly sample from this Gaussian to determine the initial network throughput 
        self._cur_bandwidth = gauss(NETWORK_THROUGHPUT_MEAN, NETWORK_THROUGHPUT_STD)

    def simulate(self, n_iters):
        for i in range(n_iters):
            # Re-sample from the gaussian to mimic changing network conditions
            self._cur_bandwidth = gauss(self._cur_bandwidth, NETWORK_THROUGHPUT_STD)

            # Choose what quality level and where to serve content from per the policy  -- currently using random one 
            next_quality_
            