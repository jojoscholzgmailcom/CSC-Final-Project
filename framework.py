import networkx as nx
import random
from delegation import Delegation
import itertools

class FrameWork():

    def __init__(self, graph: str|nx.Graph, num_nodes: int, nodeProficiency: dict[int, float]|str, delegation: Delegation, candidates = 3):
        if type(graph) == str:
            self.graph = self.__generate_graph(graph, num_nodes)
        else:
            self.graph = graph

        if type(nodeProficiency) == str:
            proficiencies = self.__generate_proficiencies(nodeProficiency, num_nodes)
        else:
            proficiencies = nodeProficiency
        
        nx.set_node_attributes(self.graph, values = proficiencies, name = "proficiency")
        self.delegation = delegation
        self.candidates = range(candidates)
        self.num_nodes = num_nodes
        
    def __generate_proficiencies(self, probability_type:str, num_nodes: int):
        proficiencies = dict()
        for idx in range(num_nodes):
            proficiencies[idx] = random.uniform(0.5, 1.0)
        return proficiencies

    def __construct_delegation_matrix(self):
        matrix = []
        for voter in range(self.num_nodes):
            matrix.append(self.__prob_delegating(voter))
        return matrix

    def __sample_delegation_matrix(self, delegation_matrix: list[list[float]]):
        voters = range(self.num_nodes)
        representatives = [Representative(voter) for voter in range(self.num_nodes)]
        for voter in range(self.num_nodes):
            representatives[voter].add_representative(random.choices(voters, weights = delegation_matrix[voter])[0], representatives)
        return {representative.voter: representative.votes for representative in representatives if not representative.did_delegate}
        
    def __sample_ranking(self, true_ranking: list[int], correct_sampling_chance: float):
        ranking = dict()
        for pairwise_comp in itertools.combinations(true_ranking, 2):
            true_comparison = true_ranking.index(pairwise_comp[0]) > true_ranking.index(pairwise_comp[1])
            ranking[pairwise_comp] = true_comparison if random.random() <= correct_sampling_chance else not true_comparison
        return ranking

    def __sum_swap_distances(self, true_ranking: list[int], ranking: list[int], representatives: dict[int, int]):
        summed_swap_dist = 0
        for representative in representatives.keys():
            summed_swap_dist += self.__swap_distance(ranking, self.__sample_ranking(true_ranking, self.graph.nodes[representative]["proficiency"])) * representatives[representative]
        return summed_swap_dist

    def __swap_distance(self, ranking: list[int], comparison_ranking: dict[tuple, bool]):
        swap_distance = 0
        for pairwise_comp in comparison_ranking.keys():
            if (ranking.index(pairwise_comp[0]) > ranking.index(pairwise_comp[1])) != comparison_ranking[pairwise_comp]:
                swap_distance += 1
        return swap_distance

    def __generate_graph(self, graph_type:str, num_nodes: int):
        match graph_type:
            case "star":
                return nx.star_graph(num_nodes - 1)
            case "cycle":
                return nx.cycle_graph(num_nodes)
            case "wheel":
                return nx.wheel_graph(num_nodes)

    def __prob_delegating(self, node: int) -> dict[int, float]:
        neighbor_proficiencies = dict()
        neighbors = nx.neighbors(self.graph, node)
        for neighbor in neighbors:
            neighbor_proficiencies[neighbor] = self.graph.nodes[neighbor]["proficiency"]
        
        delegations = self.delegation.delegation_chances((node, self.graph.nodes[node]["proficiency"]), neighbor_proficiencies)
        return [delegations.get(voter, 0.0) for voter in range(self.num_nodes)]


    def maximum_likelihood_estimation(self, true_ranking: list[int]):
        all_possible_rankings = itertools.permutations(self.candidates)
        delegation_matrix = self.__construct_delegation_matrix()
        min_swap_distance = 100000
        best_ranking = None
        for ranking in all_possible_rankings:
            summed_swap_dist = self.__sum_swap_distances(true_ranking, ranking, self.__sample_delegation_matrix(delegation_matrix))
            if summed_swap_dist < min_swap_distance:
                best_ranking = ranking
                min_swap_distance = summed_swap_dist
        return true_ranking == ranking

    def run_MLEs(self, iterations: int):
        all_possible_rankings = list(itertools.permutations(self.candidates))
        true_rankings = random.choices(all_possible_rankings, k=iterations)
        correct_iterations = 0
        for true_ranking in true_rankings:
            if self.maximum_likelihood_estimation(true_ranking):
                correct_iterations += 1
        return correct_iterations

class Representative():

    def __init__(self, voter):
        self.voter = voter
        self.votes = 1
        self.did_delegate = False
        self.end_point = voter

    def add_representative(self, representative, all_representatives):
        self.representative = representative
        self.did_delegate = self.voter != representative
        if self.did_delegate:
            final_representative = all_representatives[representative].end_point
            if final_representative != voter:
                all_representatives[final_representative].votes += self.votes
                self.end_point = final_representative
            self.votes = 0