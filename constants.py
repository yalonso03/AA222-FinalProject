"""
File: constants.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Some commonly used constants
"""


# From puffer paper experiement -- they did 2second/chunk
N_SECONDS_PER_SEGMENT = 2  #length of each chunk, in seconds


# RTT latency
    # based on a common fiber optic cable brand / calculation
    # assuming based that user is streaming from Stanford, CA
TRANSMISSION_TIME_DICT = {
    'CA': 1,  # microseconds
    'WA': 6,
    'TX': 15
}

# these are more estimates -- totally varies
    # we could incorpotate PUE or others to have this be more realistic
SERVER_EMISSION_GRAMS_PER_MB = {
    'CA' : 50,
    'WA' : 20,
    'TX' : 500
}

# needed for computing overall energy cost 
TRANSMISSION_TIME_ENERGY_CONTRIBUTION = 0.25
SERVER_EMISSIONS_ENERGY_CONTRIBUTION = 0.75



# Netflix’s 1080p can go up to 5.8 Mbps (~0.7 MB/s), but for variable streaming, these are good conservative baselines
    # pulled through end-device data for different equality levels 
    # https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10283614
    # then used Netflix's recommendations for bitrates, extrapolated for the lower ones
QUALITY_LEVELS = {
    "144p": 0.1,   # ~0.1 MB/s
    "360p": 0.3,
    "480p": 1.0,
    "720p": 2.5,
    "1080p": 4.5
}



# Maximum size of the elastic buffer, changed to SECONDS instead of MB based on lit review
    # changed it to the maximum size as cited in this paper: https://arxiv.org/abs/1808.03898
BUFFER_CAPACITY = 10


# How much it costs the server to stream one MB of content
    # assuming 1MB used (average in our quality levels)
    # referenced AWS MediaLive docs for pricing estimates: https://docs.aws.amazon.com/solutions/latest/live-streaming-on-aws/cost.html
COST_PER_MB = 0.0001


# Used to simulate noise at each timestep
NETWORK_THROUGHPUT_MEAN = 4
NETWORK_THROUGHPUT_STD = 0.4

# old values incase we screw up (these are fine too)
# NETWORK_THROUGHPUT_MEAN = 50
# NETWORK_THROUGHPUT_STD = 10

# Number of video segments used for simulations
    # this is fairly commmon, especially according to mdn web docs
N_SEGMENTS = 120