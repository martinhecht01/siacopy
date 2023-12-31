import heapq

from src.algorithms.AlgorithmABC import AlgorithmABC
from src.algorithms.AlgorithmsUtils import _UtilityNode
from src.classes.Node import Node
from src.heuristics.HeuristicCombination import HeuristicCombination
from src.heuristics.ManhattanDistance import ManhattanDistance
from src.heuristics.MinDistance import MinDistance
from src.heuristics.BipartiteHeuristic import BipartiteHeuristic


class AStar(AlgorithmABC):

    @classmethod
    def execute(cls, initial_state, heuristic_fn=None, on_state_change=None):
        if heuristic_fn is None:
            heuristic_fn = BipartiteHeuristic
        expanded_nodes = 0
        frontier = []
        heapq.heappush(frontier, _UtilityNode(Node(None, initial_state, 0), 0))
        total_cost: dict[Node, float] = {Node(None, initial_state, 0): 0}

        while frontier:
            utility_node = heapq.heappop(frontier)
            node = utility_node.node

            if (on_state_change is not None):
                on_state_change(node.state)
                
            if node.state.is_solution():
                return node, expanded_nodes, len(frontier)

            for child in node.get_children():
                new_cost = total_cost[node] + 1  # cost = 1
                if child not in total_cost or new_cost < total_cost[child]:
                    total_cost[child] = new_cost
                    priority = new_cost + heuristic_fn.calculate(child.state)
                    heapq.heappush(frontier, _UtilityNode(child, priority))

            expanded_nodes += 1
        return None
