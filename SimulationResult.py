"""
File: SimulationResult.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Defines a class that I use for cleanliness to store the output of a simulation (basically just a struct)
"""

class SimulationResult:
    def __init__(self, quality_hist, average_quality, total_rebuffer_time, num_rebuffer_events, carbon_emitted, total_cost):
        self.quality_history = quality_hist
        self.average_quality = average_quality
        self.total_rebuffer_time = total_rebuffer_time
        self.num_rebuffer_events = num_rebuffer_events
        self.carbon_emitted = carbon_emitted
        self.total_cost = total_cost