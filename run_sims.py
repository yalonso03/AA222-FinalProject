"""
File: run_sims.py
By: Yasmine Alonso (yalonso) and Kate Baker (kesbaker)
For: AA222 (Engineering Design Optimization) Final Project
----------------------------------------------------------
Runs simulations for our final project to test how a variety of methods perform!
"""

from NetworkSimulator import NetworkSimulator
import constants
import policies
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import numpy as np
import random
import sys


# use this dictionary to loop through the multiple plotting
policy_dict = {
    "simple": policies.simple_quality_policy,
    "cross_entropy": policies.cross_entropy_policy,
    "random": policies.random_policy,
    "maximum": policies.always_max_quality,
    "minimum": policies.always_min_quality
}

# initial segments to try
# N_SEGMENTS = 20


# testing! 20 segments with a random policy
simulator = NetworkSimulator(20, policies.simple_quality_policy)
res = simulator.simulate()  # returns SimulationResult object
# print(res.average_quality)
# print(res.quality_history)
# obviously i'd want to print more stats but just wanted to test


def quality_over_time_comparison(results, labels, num_segments=constants.N_SEGMENTS):
    """
    Plots the quality levels over time for each policy on the same chart.
    
    Args:
        num_segments (int): how many segments to simulate
        policy_dict (dict): mapping of {label: policy_function}
    """
    plt.figure()

    for i in range(len(results)):
        label = labels[i]
        res = results[i]
        plt.plot(res.quality_history, marker='o', label=label)


    # for label, policy in policy_dict.items():
    #     random.seed(331703)  #birthdays hehehe, ensures that each simulation run with a different policy has the same stream of randomness generated
    #     simulator = NetworkSimulator(num_segments, policy)
    #     res = simulator.simulate()
    #     plt.plot(res.quality_history, marker='o', label=label)

    plt.title("Quality Level Over Time by Policy")
    plt.xlabel("Segment #")
    plt.ylabel("Quality (Mbps)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("quality_over_time_comparison.png")
    plt.show()


def quality_choice_hist_comparison(simulation_results, labels):
    """
    Compares how different policies distribute their quality choices.
    Plots a grouped bar chart with frequency of each quality level per policy.

    Parameters:
    - simulation_results: List of SimulationResult objects
    - labels: List of corresponding policy labels (strings)
    """

    if len(simulation_results) != len(labels):
        raise ValueError("simulation_results and labels must be the same length")

    quality_levels = sorted(set(constants.QUALITY_LEVELS.values()))
    data = defaultdict(list)  # quality level → list of counts (one per policy)

    for res in simulation_results:
        counts = Counter(res.quality_history)
        for q in quality_levels:
            data[q].append(counts.get(q, 0))  # fill in 0 if this quality wasn't chosen

    # Plotting grouped bar chart
    x = np.arange(len(quality_levels))  # group positions
    width = 0.8 / len(simulation_results)  # bar width based on number of policies

    plt.figure()
    for i, label in enumerate(labels):
        heights = [data[q][i] for q in quality_levels]
        plt.bar(x + i * width, heights, width=width, label=label)

    plt.title("Distribution of Quality Levels by Policy")
    plt.xlabel("Quality (Mbps)")
    plt.ylabel("Frequency")
    plt.xticks(x + width * (len(simulation_results) - 1) / 2, quality_levels)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("quality_histogram_comparison.png")
    plt.show()



def compare_co2_hist(results, labels, num_segments=constants.N_SEGMENTS):
    """
    Takes a dictionary of {label: policy_fn}, runs each, and plots all emissions together.
    """
    # labels = []
    emissions = [result.carbon_emitted for result in results]

    # for label, policy in policy_dict.items():
    #     #simulator = NetworkSimulator(num_segments, policy)
    #     #res = simulator.simulate()
    #     #labels.append(label)
    #     emissions.append(res.carbon_emitted)

    plt.bar(labels, emissions)
    plt.ylabel("Total CO₂ Emitted")
    plt.title("Carbon Emissions Comparison")
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig("carbon_emissions_comparison.png")
    plt.show()



def plot_four_objective_radar(results, labels):
    """
    Generates a radar plot demonstrating the 4 objectives we're trying to achieve:
    - Minimized CO2 emissions
    - Minimized cost ($)
    - Minimized rebuffer time
    - Maximized streaming quality

    Args:
        results (List[SimulationResult]): List of SimulationResults that comes from running sims
        labels (List[string]): List of string labels of the policy types that we are testing

    Refernces:
    - Used ChatGPT to write plotting code
    """
    # Extract raw data
    avg_quality = np.array([r.average_quality for r in results])
    inv_rebuffers = np.array([1 / r.total_rebuffer_time if r.total_rebuffer_time > 0 else 0 for r in results])
    inv_carbon = np.array([1 / r.carbon_emitted if r.carbon_emitted > 0 else 0 for r in results])
    inv_cost = np.array([1 / r.total_cost if r.total_cost > 0 else 0 for r in results])

    # Stack them for easier normalization
    data = np.stack([avg_quality, inv_rebuffers, inv_carbon, inv_cost], axis=1)

    # Normalize each column to [0, 1]
    min_vals = data.min(axis=0)
    max_vals = data.max(axis=0)
    ranges = max_vals - min_vals
    normalized = (data - min_vals) / np.where(ranges == 0, 1, ranges)

    # Set up the radar plot
    num_vars = 4
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # loop back to start

    categories = [
        "Avg Quality",
        "1 / Time rebuffering",
        "1 / Carbon Emitted",
        "1 / Total Cost"
    ]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i, (row, label) in enumerate(zip(normalized, labels)):
        values = row.tolist()
        values += values[:1]  # close the loop
        ax.plot(angles, values, label=label)
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    ax.set_title("Policy Comparison on 4 Objectives", size=14)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.show()

def create_plots(simulation_results, labels, num_segments):
    plot_four_objective_radar(simulation_results, labels)
    compare_co2_hist(simulation_results, labels, num_segments)
    quality_over_time_comparison(simulation_results, labels, num_segments)
    quality_choice_hist_comparison(simulation_results, labels)


def simulate_policies(num_segments, policy_dict, verbose=False, plots=False):
    simulation_results = []
    for label, policy in policy_dict.items():
        random.seed(331703)  #birthdays hehehe, ensures that each simulation run with a different policy has the same stream of randomness generated
        simulator = NetworkSimulator(num_segments, policy)
        res = simulator.simulate()
        simulation_results.append(res)
        if verbose:
            print("")
            print(f"---------------------------------------------------------")
            print(f"Completed simulations for {label}.....")
            print(f"    Quality history: {res.quality_history}")
            print(f"    CO2 emitted: {res.carbon_emitted}")
            print(f"    # of rebuffers: {res.num_rebuffer_events}")
            print(f"    Total cost ($): {res.total_cost}")
            print(f"---------------------------------------------------------")
            print("")

    labels = list(policy_dict.keys())

    # Create all desired plots
    if plots:
        create_plots(simulation_results, labels, num_segments)



def main():
    args = sys.argv[1:] 

    # -v for verbose (prints more output to console)
    # -p for generating plots
    valid_flags = {"-v", "-p"}
    if any(arg not in valid_flags for arg in args) or len(args) > 2:
        raise ValueError("Incorrect usage. Valid flags are '-v' and '-p'. Use like: `python3 run_sims.py -v -p`")

    verbose = "-v" in args
    plots = "-p" in args

    simulate_policies(constants.N_SEGMENTS, policy_dict, verbose=verbose, plots=plots)




if __name__ == "__main__":
    main()
