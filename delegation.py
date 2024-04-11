import random

class Delegation():
    

    def __init__(self, exogenous_probability: float = 0.2):
        
        # The probability that a voter will delegate to a neighbor
        if exogenous_probability:
            self.exogenous_probability = exogenous_probability

    # Return a dictionary with the chances that the voter delegates to that voter (also include chances of delegating to himself)
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        pass

    
    def approve_neighbors(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float], alpha = 0.15) -> dict[int, bool]:
        approved_neighbors = dict()
        for neighbor, proficiency in neighbor_proficiencies.items():
            if proficiency >= own_proficiency[1] + alpha:
                approved_neighbors[neighbor] = proficiency
            else:
                continue
        return approved_neighbors


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
    
class RandomApprovedNeighborDelegation(Delegation):
    # If there are no approved neighbors, the voter will delegate to himself, otherwise it will delegate to a random approved neighbor
    
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        approved_neighbors = super().approve_neighbors(own_proficiency, neighbor_proficiencies)
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        if len(approved_neighbors) == 0:
            delegation_probs[own_proficiency[0]] = 1.0
        else:
            delegation_probs[random.choice(list(approved_neighbors.keys()))] = 1.0
        return delegation_probs

        
class RandomMoreApprovedNeighborsDelegation(Delegation):
    # If there are no approved neighbors or the number of approved neighbors is less than the number of non-approved neighbors, the voter will delegate to himself, otherwise it will delegate to a random approved neighbor
        
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        approved_neighbors = super().approve_neighbors(own_proficiency, neighbor_proficiencies)
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        if len(approved_neighbors) != 0:
            if len(approved_neighbors) < len(neighbor_proficiencies) - len(approved_neighbors) :
                delegation_probs[random.choice(list(approved_neighbors.keys()))] = 1.0
            else:
                delegation_probs[own_proficiency[0]] = 1.0
        else:
            delegation_probs[own_proficiency[0]] = 1.0
        return delegation_probs


class SingleApprovedNeighbourDelegation(Delegation):
    # If there are no approved neighbors, the voter will delegate to himself, otherwise it will delegate to the first approved neighbor in the voter's local ordering
            
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        approved_neighbors = super().approve_neighbors(own_proficiency, neighbor_proficiencies)
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        if len(approved_neighbors) == 0:
            delegation_probs[own_proficiency[0]] = 1.0
        else:
            first_approved_neighbor = max(approved_neighbors, key=approved_neighbors.get)
            delegation_probs[first_approved_neighbor] = 1.0
        return delegation_probs
    
    
class LocalStrictlyUpwardDelegation(Delegation):
    # If the voter delegates, it will delegate to an approved neighbor chosen uniformly at random, otherwise it will delegate to itself
            
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        approved_neighbors = super().approve_neighbors(own_proficiency, neighbor_proficiencies)
        delegation = random.choices([0, 1], weights = [1 - self.exogenous_probability, self.exogenous_probability])[0]
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}
        if delegation == 0:  
            delegation_probs[own_proficiency[0]] = 1.0
        else:
            if len(approved_neighbors) != 0:
                for neighbor in approved_neighbors:
                    delegation_probs[neighbor] = 1.0
            else:
                delegation_probs[own_proficiency[0]] = 1.0
        return delegation_probs
    
    
class LocalConfidenceBasedDelegation(Delegation):
    # If the voter delegates, it will delegate to a neighbor chosen uniformly at random, otherwise it will delegate to itself
    # The probability of delegating to a neighbor is inversely propotional to the voter's proficiency
    
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        delegation = random.choices([0, 1], weights = [own_proficiency[1], 1 - own_proficiency[1]])[0]
        if delegation == 0:
            delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}  
            delegation_probs[own_proficiency[0]] = 1.0
        else:
            delegation_probs = {voter:1.0 for voter in neighbor_proficiencies}
            delegation_probs[own_proficiency[0]] = 0.0
        return delegation_probs
    

class LocalCountinousDelegation(Delegation):
    # If the voter delegates, it will delegate to a neighbor chosen depending on the neighbor's proficiency, otherwise it will delegate to itself
    # The probability of delegating to a neighbor is inversely propotional to the voter's proficiency 
    
    def delegation_chances(self, own_proficiency: tuple[int, float], neighbor_proficiencies: dict[int, float]) -> dict[int, float]:
        delegation = random.choices([0, 1], weights = [own_proficiency[1], 1 - own_proficiency[1]])[0]
        delegation_probs = {voter:0.0 for voter in neighbor_proficiencies}  
        if delegation == 0:
            delegation_probs[own_proficiency[0]] = 1.0
        else:
            delegation_probs[own_proficiency[0]] = 0.0
            for neighbor, proficiency in neighbor_proficiencies.items():
                delegation_probs[neighbor] = proficiency
        return delegation_probs