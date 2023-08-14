from collections import defaultdict
class BFS:
    @staticmethod
    def bfs(initial_state):
        steps = 0
        visited = []
        queue = []
        queue.append(initial_state)
        while queue:
            state = queue.pop(0)
            if state.is_solution():
                print("Solution found in ", steps, " steps using BFS")
                return state
            if state not in visited:
                visited.append(state)
                for child in state.get_children():
                    queue.append(child)
            steps += 1
        return None
