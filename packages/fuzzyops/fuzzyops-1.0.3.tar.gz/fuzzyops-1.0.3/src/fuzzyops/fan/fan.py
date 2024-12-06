from typing import List
from fuzzyops.fuzzy_numbers import Domain, FuzzyNumber


class Node:
    def __init__(self, name):
        self.name = name
        self.in_edges = []
        self.out_edges = []

    def add_in_edge(self, edge):
        self.in_edges.append(edge)

    def add_out_edge(self, edge):
        self.out_edges.append(edge)


class Edge:
    def __init__(self, start_node, end_node, weight):
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight
        self.start_node.add_out_edge(self)
        self.end_node.add_in_edge(self)


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_name):
        if node_name not in self.nodes:
            new_node = Node(node_name)
            self.nodes[node_name] = new_node
        return self.nodes[node_name]

    def add_edge(self, start_node_name, end_node_name, weight):
        start_node = self.add_node(start_node_name)
        end_node = self.add_node(end_node_name)
        new_edge = Edge(start_node, end_node, weight)
        self.edges.append(new_edge)

    def get_paths_from_to(self, start_node_name, end_node_name):
        # Возвращает список всех возможных путей от start_node до end_node
        paths = []
        stack = [(start_node_name, [])]
        while stack:
            current_node, path = stack.pop()
            if current_node == end_node_name:
                paths.append(path + [current_node])
            else:
                for edge in self.nodes[current_node].out_edges:
                    if edge.end_node.name not in path:
                        stack.append((edge.end_node.name, path + [current_node]))
        return paths

    def calculate_path_fuzziness(self, path):
        fuzziness = 1.0
        for i in range(len(path) - 1):
            start_node = path[i]
            end_node = path[i + 1]
            edges = [edge for edge in self.edges if
                     edge.start_node.name == start_node and edge.end_node.name == end_node]
            if len(edges) == 0:
                raise ValueError("Path is invalid")
            min_weight = min([edge.weight for edge in edges])
            fuzziness *= min_weight
        return fuzziness

    def find_most_feasible_path(self, start_node_name, end_node_name):
        paths = self.get_paths_from_to(start_node_name, end_node_name)
        feasible_paths = [(path, self.calculate_path_fuzziness(path)) for path in paths]
        sorted_paths = sorted(feasible_paths, key=lambda x: x[1], reverse=True)
        return sorted_paths[0][0] if sorted_paths else None

    def macro_algorithm_for_best_alternative(self):
        # Макроалгоритм для выбора наиболее осуществимой альтернативы сетевой модели
        best_alternative = None
        max_feasibility = 0.0
        for start_node in self.nodes.values():
            for end_node in self.nodes.values():
                if start_node != end_node:
                    most_feasible_path = self.find_most_feasible_path(start_node.name, end_node.name)
                    if most_feasible_path:
                        path_feasibility = self.calculate_path_fuzziness(most_feasible_path)
                        if path_feasibility > max_feasibility:
                            max_feasibility = path_feasibility
                            best_alternative = most_feasible_path
        return best_alternative, max_feasibility


def calc_final_scores(f_nums: List[FuzzyNumber]):
    res = 1
    for f_num in f_nums:
        res *= f_num
    return res.defuzz()
