from delegation import SelfDelegation
from delegation import HighestDelegation
from delegation import RandomApprovedNeighborDelegation
from delegation import RandomMoreApprovedNeighborsDelegation
from delegation import SingleApprovedNeighbourDelegation
from delegation import LocalStrictlyUpwardDelegation
from delegation import LocalConfidenceBasedDelegation
from delegation import LocalCountinousDelegation
from framework import FrameWork
import random

if __name__ == "__main__":
    
    delegation_list = [ HighestDelegation(), RandomApprovedNeighborDelegation(), RandomMoreApprovedNeighborsDelegation(), SingleApprovedNeighbourDelegation(), LocalStrictlyUpwardDelegation(), LocalConfidenceBasedDelegation(), LocalCountinousDelegation()]
    voters_list = [5, 10]
    total_runs = 1000
    
    for delegation in delegation_list:
        for voters in voters_list:
        # genetate the random proficiencies for the voters
            voters_proficiencies = {voter: random.uniform(0.5, 1.0) for voter in range(voters)}
            baseline_delegation = FrameWork("star", voters, voters_proficiencies, SelfDelegation())
            test_delegation  = FrameWork("star", voters, voters_proficiencies, delegation)
            gain = (test_delegation.run_MLEs(total_runs) - baseline_delegation.run_MLEs(total_runs)) / total_runs * 100.0
            print(f"Delegation: {delegation.__class__.__name__}, Voters: {voters}, Gain: {gain:.3}")