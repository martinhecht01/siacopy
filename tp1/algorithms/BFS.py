from collections import deque

from classes.Node import Node


class BFS:
    @staticmethod
    def bfs(initial_state):
        size = 0
        visited = set()
        queue = deque()
        root = Node(None, initial_state)
        queue.append(root)
        while queue:
            node = queue.popleft()
            if node.state.is_solution():
                return node, size

            if node not in visited:
                visited.add(node)
                for child in node.get_children():
                    queue.append(child)

            size += 1

        return None
