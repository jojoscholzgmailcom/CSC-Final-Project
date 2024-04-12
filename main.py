from delegation import HighestDelegation, RandomApprovedNeighborDelegation, RandomMoreApprovedNeighborsDelegation, SingleApprovedNeighbourDelegation, LocalStrictlyUpwardDelegation, LocalConfidenceBasedDelegation, LocalCountinousDelegation, SelfDelegation, Delegation
from framework import FrameWork
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_gains(gains_per_graph_and_delegation: dict[tuple[str, str], list[float]], graph_types: list[str], delegation_list: list[str]):
    for graph in graph_types:
        fig, ax = plt.subplots(constrained_layout=True)
        pallete = sns.color_palette("tab10")
        for delegation in delegation_list:
            sns.lineplot(data=gains_per_graph_and_delegation[(graph, delegation)], label = delegation, color=pallete[delegation_list.index(delegation)])
        sns.lineplot(data=[0.0 for _ in range(10)], label="Baseline", linestyle= ':', color='black', alpha=0.5)
        ax.set_xticks(np.arange(0, 10, 1))
        ax.set_title(f"Average gain over 1000 runs for 10 epochs for {graph} graph")
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Gain')
        plt.legend().set_visible(False)
        fig.legend(loc='outside upper right')
        plt.savefig(f"final_gain_{graph}.png")    
    return
    
def run_simulations(voters: int, total_runs: int, graph_types: list[str], delegation_list: list[Delegation], epochs: int = 10):
    gains_per_graph_and_delegation = dict()
    for epoch in range(epochs):
            voters_proficiencies = {voter: random.uniform(0.5, 1.0) for voter in range(voters)}
            for graph in graph_types:
                for delegation in delegation_list:
                        baseline_delegation = FrameWork(graph, voters, voters_proficiencies, SelfDelegation())
                        test_delegation  = FrameWork(graph, voters, voters_proficiencies, delegation)
                        gain = (test_delegation.run_MLEs(total_runs) - baseline_delegation.run_MLEs(total_runs)) / total_runs
                        if epoch == 0:
                            gains_per_graph_and_delegation[(graph, delegation.__class__.__name__)] = [gain]
                        else:
                            gains_per_graph_and_delegation[(graph, delegation.__class__.__name__)].append(gain)
    return gains_per_graph_and_delegation
    


if __name__ == "__main__":
    
    delegation_list = [HighestDelegation(), RandomApprovedNeighborDelegation(), RandomMoreApprovedNeighborsDelegation(), SingleApprovedNeighbourDelegation(), LocalStrictlyUpwardDelegation(), LocalConfidenceBasedDelegation(), LocalCountinousDelegation()]
    graph_types = ["star", "wheel", "cycle"]
    voters = 50
    total_runs = 1000
    
    gains_per_graph_and_delegation = run_simulations(voters, total_runs, graph_types, delegation_list)
    plot_gains(gains_per_graph_and_delegation, graph_types, [delegation.__class__.__name__ for delegation in delegation_list])                        