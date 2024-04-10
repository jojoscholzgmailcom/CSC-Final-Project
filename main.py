from delegation import SelfDelegation
from delegation import HighestDelegation
from delegation import RandomApprovedNeighborDelegation
from delegation import RandomMoreApprovedNeighborDelegation
from delegation import SingleApprovedNeighbourDelegation
from framework import FrameWork

if __name__ == "__main__":
    #delegation = SelfDelegation()
    #delegation = HighestDelegation()
    delegation = SingleApprovedNeighbourDelegation()
    #framework = FrameWork("star", 3, "random", delegation)
    framework = FrameWork("star", 5, {0: 0.9, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.8}, delegation)
    total_runs = 10
    correct_runs = framework.run_MLEs(total_runs)
    print(f"{correct_runs} out of {total_runs}, were correct which gives an accuracy of {(correct_runs/total_runs*100.0):.3}")