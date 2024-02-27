# Araullo, John Art Marie G.
# BSCS-NS-3A
# CS321L-M - Artificial Intelligence
# Machine Problem #1
# Create an Problem Solving Agent to Solve the Fox, Chicken and Grain Problem
# Algorithm: BFS - Breadth First Search

from collections import deque

class State:
    def __init__(self, farmer, fox, chicken, grain):
        self.farmer = farmer
        self.fox = fox
        self.chicken = chicken
        self.grain = grain

    def is_valid(self):
        # Check constraints for a valid state
        if self.chicken == self.grain and self.chicken != self.farmer:
            return False
        if self.fox == self.chicken and self.fox != self.farmer:
            return False
        return True

    def is_goal(self):
        return all(attr == '1' for attr in [self.farmer, self.fox, self.chicken, self.grain])

    def __eq__(self, other):
        return all(getattr(self, attr) == getattr(other, attr) for attr in ['farmer', 'fox', 'chicken', 'grain'])

    def __hash__(self):
        return hash(tuple(getattr(self, attr) for attr in ['farmer', 'fox', 'chicken', 'grain']))

    def __str__(self):
        return f"Farmer: {self.farmer}, Fox: {self.fox}, Chicken: {self.chicken}, Grain: {self.grain}"


def generate_next_states(current_state):
    next_states = []

    farmer, fox, chicken, grain = current_state.farmer, current_state.fox, current_state.chicken, current_state.grain

    # VALID MOVES
    # Farmer is with the chicken first.
    if farmer == chicken:
        next_states.append(State('1' if farmer == '0' else '0', fox, '1' if chicken == '0' else '0', grain))

    # Farmer is with the fox.
    if farmer == fox:
        next_states.append(State('1' if farmer == '0' else '0', '1' if fox == '0' else '0', chicken, grain))

    # Farmer is with the chicken and not with the fox.
    if farmer == chicken and farmer != fox:
        next_states.append(State('1' if farmer == '0' else '0', '1' if fox == '0' else '0',
                                 '1' if chicken == '0' else '0', grain))

    # Farmer leaves the chicken.
    if farmer == chicken:
        next_states.append(State('1' if farmer == '0' else '0', fox, '1' if chicken == '0' else '0', grain))

    # Farmer is with the grain.
    if farmer == grain:
        next_states.append(State('1' if farmer == '0' else '0', fox, chicken, '1' if grain == '0' else '0'))

    # Farmer gets chicken again.
    if farmer == chicken:
        next_states.append(State('1' if farmer == '0' else '0', fox, '1' if chicken == '0' else '0', grain))

    return [state for state in next_states if state.is_valid()]

def bfs(initial_state):
    queue = deque()
    visited = set()
    queue.append((initial_state, []))

    while queue:
        current_state, path = queue.popleft()

        if current_state.is_goal():
            return path + [current_state]

        visited.add(current_state)

        next_states = generate_next_states(current_state)

        for next_state in next_states:
            if next_state not in visited:
                queue.append((next_state, path + [current_state]))

    return None

def main():
    initial_state = State('0', '0', '0', '0')

    solution = bfs(initial_state)

    if solution:
        print("Solution found:")
        for i, step in enumerate(solution):
            print(f"Step {i + 1}: {step}")
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()
