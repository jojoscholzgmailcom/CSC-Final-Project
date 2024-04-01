

class Delegation():

    def __init__(self):
        pass

    # Return a dictionary with the chances that the voter delegates to that voter (also include chances of delegating to himself)
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        pass


class SelfDelegation():

    # Return a dictionary with the chances that the voter delegates to that voter (also include chances of delegating to himself)
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        delegation_probs[own_proficiency[0]] = 1.0
        return delegation_probs

class HighestDelegation():

    # Return a dictionary with the chances that the voter delegates to that voter (also include chances of delegating to himself)
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        max_proficiency = own_proficiency[1]
        max_voter = own_proficiency[0]
        for neighbor, proficiency in neighbor_proficiencies.items():
            if proficiency > max_proficiency:
                max_voter = neighbor
                max_proficiency = proficiency

        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        delegation_probs[own_proficiency[0]] = 0.0
        delegation_probs[max_voter] = 1.0
        return delegation_probs