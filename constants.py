"""
File: constants.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Some commonly used constants
"""

#TODO @KATE all of these constants are bullshit values. None of them are legitimate -- we need to do research to inform what would
# be a good realistic value to set them to 

N_SECONDS_PER_SEGMENT = 2  #length of each chunk, in seconds

# Tons (?) of CO2 per _____ ? need to figure it out 
LOCATIONS_CO2_DICT = {
    'CA' : 50,
    'WA' : 20,
    'TX' : 500
}


# Can add more, I think TY said they realistically use 7-8
QUALITY_LEVELS = {
    "LOW" : 0.3,  # 0.3 MB/sec
    "MEDIUM" : 0.5,
    "HIGH" : 1.0
}

# Maximum size of the elastic buffer, in MB
BUFFER_CAPACITY = 20  #TODO NOT SURE WHAT SIZES ARE NORMAL

COST_PER_MB = 0.01 

# Used to simulate noise at each timestep
NETWORK_THROUGHPUT_MEAN = 50
NETWORK_THROUGHPUT_STD = 10