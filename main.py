from delegation import SelfDelegation
from framework import FrameWork

if __name__ == "__main__":
    delegation = SelfDelegation()
    framework = FrameWork("star", 100, "random", delegation)
    total_runs = 1000
    correct_runs = framework.run_MLEs(total_runs)
    print(f"{correct_runs} out of {total_runs}, were correct which gives an accuracy of {(correct_runs/total_runs*100.0):.3}")