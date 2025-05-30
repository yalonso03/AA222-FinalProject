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
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import numpy as np

# todo I’m not sure how u did the simulation runs, but we should make sure that the network bandwidth at each time step is the same 


# use this dictionary to loop through the multiple plotting
policy_dict = {
    "simple": policies.simple_quality_policy,
    "cross_entropy": policies.cross_entropy_policy,
    "random": policies.cross_entropy_policy,
    "maximum": policies.always_max_quality,
    "minimum": policies.always_min_quality
}

# initial segments to try
N_SEGMENTS = 20


# testing! 20 segments with a random policy
simulator = NetworkSimulator(20, policies.simple_quality_policy)
res = simulator.simulate()  # returns SimulationResult object
print(res.average_quality)
print(res.quality_history)
# obviously i'd want to print more stats but just wanted to test


def quality_over_time_comparison(num_segments, policy_dict):
    """
    Plots the quality levels over time for each policy on the same chart.
    
    Args:
        num_segments (int): how many segments to simulate
        policy_dict (dict): mapping of {label: policy_function}
    """
    plt.figure()

    for label, policy in policy_dict.items():
        simulator = NetworkSimulator(num_segments, policy)
        res = simulator.simulate()
        plt.plot(res.quality_history, marker='o', label=label)

    plt.title("Quality Level Over Time by Policy")
    plt.xlabel("Segment #")
    plt.ylabel("Quality (Mbps)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("quality_over_time_comparison.png")
    plt.show()




def quality_choice_hist_comparison(num_segments, policy_dict):
    """
    Compares how different policies distribute their quality choices.
    Plots a grouped bar chart with frequency of each quality level per policy.
    """

    # Collect all results
    quality_levels = sorted(set(val for val in constants.QUALITY_LEVELS.values()))
    data = defaultdict(list)  # quality level → list of counts (one per policy)

    policy_names = []

    for label, policy in policy_dict.items():
        simulator = NetworkSimulator(num_segments, policy)
        res = simulator.simulate()
        counts = Counter(res.quality_history)
        policy_names.append(label)

        for q in quality_levels:
            data[q].append(counts.get(q, 0))  # fill in 0 if this quality wasn't chosen

    # Plotting grouped bar chart
    x = np.arange(len(quality_levels))  # group positions
    width = 0.8 / len(policy_dict)      # bar width based on number of policies

    plt.figure()
    for i, label in enumerate(policy_names):
        heights = [data[q][i] for q in quality_levels]
        plt.bar(x + i * width, heights, width=width, label=label)

    plt.title("Distribution of Quality Levels by Policy")
    plt.xlabel("Quality (Mbps)")
    plt.ylabel("Frequency")
    plt.xticks(x + width * (len(policy_dict) - 1) / 2, quality_levels)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("quality_histogram_comparison.png")
    plt.show()



def compare_co2_hist(num_segments, policy_dict):
    """
    Takes a dictionary of {label: policy_fn}, runs each, and plots all emissions together.
    """
    labels = []
    emissions = []

    for label, policy in policy_dict.items():
        simulator = NetworkSimulator(num_segments, policy)
        res = simulator.simulate()
        labels.append(label)
        emissions.append(res.carbon_emitted)

    plt.bar(labels, emissions)
    plt.ylabel("Total CO₂ Emitted")
    plt.title("Carbon Emissions Comparison")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("carbon_emissions_comparison.png")
    plt.show()



def main():

    quality_over_time_comparison(N_SEGMENTS, policy_dict)
    quality_choice_hist_comparison(N_SEGMENTS, policy_dict)
    compare_co2_hist(N_SEGMENTS, policy_dict)



if __name__ == "__main__":
    main()
