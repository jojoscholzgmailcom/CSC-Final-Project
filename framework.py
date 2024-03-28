import networkx as nx
import random
from delegation import Delegation

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
        
        
    def __generate_proficiencies(self, probability_type:str, num_nodes: int):
        proficiencies = dict()
        for idx in range(num_nodes):
            proficiencies[idx] = random.uniform(0.5, 1.0)
        return proficiencies

    def __generate_graph(self, graph_type:str, num_nodes: int):
        match graph_type:
            case "star":
                return nx.star_graph(num_nodes)
            case "cycle":
                return nx.cycle_graph(num_nodes)
            case "wheel":
                return nx.wheel_graph(num_nodes)