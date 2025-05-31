"""
File: NetworkSimulator.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Defines a simulator class for our problem!
"""
from random import gauss
import policies
import constants  # defines constants that are used across multiple files, eg quality levels, server locations, distances from servers etc
from SimulationResult import SimulationResult


"""
Kate recap notes (can delete)

- class for simulating a network, takes in number of segments (2 second long clips) to be sent for the whole movie (aka like a movie could be divided into 100 2 second clips). 
    - we also pass in a functio nthat returns the next QUALITY level to use (we will us the optimization strats to figure this out)

- the init sets up everything mostly set to zero but then a current bandwidth that flucates (do guass for mean/std)

- in simulate, we take the results from our policy and calculate what made it change
    - using quality, we then figure out if the time to download had the buffer drain in the meantime. if so, we add to the times we needed to buffer/jitter


"""


class NetworkSimulator:
    def __init__(self, n_segments, policy):
        """Initializes the NetworkSimulator class 

        Args:
            n_segments (int): number of 2-second long clips to be sent for this specific movie
            policy (function): function that takes in features of the network and returns the next quality level to use for adaptive streaming and the next server location.
        """
        self._n_segments = n_segments
        self._policy = policy
        self._cur_bandwidth = gauss(constants.NETWORK_THROUGHPUT_MEAN, constants.NETWORK_THROUGHPUT_STD)
        self._num_sec_in_buffer = 0
        self._prev_quality_level = None
        self._n_rebuffers = 0
        self._total_rebuffer_time = 0.0
        self._carbon_emitted = 0.0
        self._total_cost = 0.0
        self._quality_history = []

    def simulate(self):
        for _ in range(self._n_segments):
        
            # update the simulated current bandwidth of the network we're on, using the mean as the old bandwidth, with a set STD
            self._cur_bandwidth = max(0.01, gauss(self._cur_bandwidth, constants.NETWORK_THROUGHPUT_STD))  # prevent 0

            # query our policy (one of the functions defined in policies.py) 
            quality, server_loc = self._policy(self._cur_bandwidth, self._num_sec_in_buffer, self._prev_quality_level, self._n_rebuffers)

            # quality of the segment is in units of Megabytes per sec
            # seconds per segment is in units of sec
            # determine the size of the segment in megabytes
            segment_size_MB = quality * constants.N_SECONDS_PER_SEGMENT

            time_to_download_s = segment_size_MB / self._cur_bandwidth
            if self._num_sec_in_buffer >= time_to_download_s:
                self._num_sec_in_buffer -= time_to_download_s
                rebuffer_time = 0.0
                # in this case buffer drained normally, there was never a lack of material in buffer
            else:
                # here the buffer was not long enough, so we had to rebuffer one time
                rebuffer_time = time_to_download_s - self._num_sec_in_buffer
                self._n_rebuffers += 1
                self._total_rebuffer_time += rebuffer_time
                self._num_sec_in_buffer = 0.0  # empty buffer while waiting
            self._num_sec_in_buffer = min(self._num_sec_in_buffer + constants.N_SECONDS_PER_SEGMENT, constants.BUFFER_CAPACITY) # we treat buffer as seconds

            # todo might need to return to this if we want the policies to consider transmission time, too
            total_carbon_emitted_in_choice = (constants.SERVER_EMISSION_GRAMS_PER_MB[server_loc] * constants.SERVER_EMISSIONS_ENERGY_CONTRIBUTION) + (constants.TRANSMISSION_TIME_DICT[server_loc] * constants.TRANSMISSION_TIME_ENERGY_CONTRIBUTION)
            # self._carbon_emitted += constants.LOCATIONS_CO2_DICT[server_loc] * segment_size_MB  #increment total co2 emitted
            self._carbon_emitted += total_carbon_emitted_in_choice
            self._total_cost += segment_size_MB * constants.COST_PER_MB  #increment total cost
            self._quality_history.append(quality)  # keep track of previous qualities
            self._prev_quality_level = quality

        avg_quality = sum(self._quality_history) / len(self._quality_history)
        return SimulationResult(self._quality_history, avg_quality, self._total_rebuffer_time, self._n_rebuffers, self._carbon_emitted, self._total_cost)