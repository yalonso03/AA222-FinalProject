"""
File: run_sims.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Runs simulations for our final project!
"""

from NetworkSimulator import NetworkSimulator
import constants
import policies

# testing! 20 segments with a random policy
simulator = NetworkSimulator(20, policies.cross_entropy_policy)
res = simulator.simulate()  # returns SimulationResult object
print(res.average_quality)
print(res.quality_history)
# obviously i'd want to print more stats but just wanted to test