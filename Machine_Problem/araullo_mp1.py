# Araullo, John Art Marie G.
# BSCS-NS-3A
# CS321L-M - Artificial Intelligence
# Machine Problem #1
# Create an Problem Solving Agent to Solve the Fox, Chicken and Grain Problem
# Algorithm: BFS - Breadth First Search

from collections import deque

# Define the initial state and goal state
initial_state = {'farmer': 'left', 'fox': 'left', 'chicken': 'left', 'grain': 'left'}
goal_state = {'farmer': 'right', 'fox': 'right', 'chicken': 'right', 'grain': 'right'}

# Print the initial and goal states for verification
print("Initial State:", initial_state)
print("Goal State:", goal_state)

# Define the valid moves
valid_moves = [
    {'farmer': 'left', 'fox': 0, 'chicken': 0, 'grain': 0},
    {'farmer': 'left', 'fox': -1, 'chicken': 0, 'grain': 0},
    {'farmer': 'left', 'fox': 0, 'chicken': -1, 'grain': 0},
    {'farmer': 'left', 'fox': 0, 'chicken': 0, 'grain': -1},
    {'farmer': 'right', 'fox': 0, 'chicken': 0, 'grain': 0},
    {'farmer': 'right', 'fox': -1, 'chicken': 0, 'grain': 0},
    {'farmer': 'right', 'fox': 0, 'chicken': -1, 'grain': 0},
    {'farmer': 'right', 'fox': 0, 'chicken': 0, 'grain': -1}
]
# 1. Move the farmer to the left without taking any other item.
# 2. Move the farmer and the fox to the left while leaving the chicken and grain behind.
# 3. Move the farmer and the chicken to the left while leaving the fox and grain behind.
# 4. Move the farmer and the grain to the left while leaving the fox and chicken behind.
# 5. Move the farmer to the right without taking any other item.
# 6. Move the farmer and the fox to the right while leaving the chicken and grain behind.
# 7. Move the farmer and the chicken to the right while leaving the fox and grain behind.
# 8. Move the farmer and the grain to the right while leaving the fox and chicken behind.

def is_valid(state):
    if state['chicken'] == state['grain'] and state['farmer'] != state['chicken']:
        return False
    if state['fox'] == state['chicken'] and state['farmer'] != state['fox']:
        return False
    return True

def bfs():
    queue = deque()
    visited = set()

    queue.append((initial_state, []))

    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        visited.add(tuple(current_state.values()))

        for move in valid_moves:
            new_state = current_state.copy()
            for key, value in move.items():
                if key != 'farmer':
                    new_state[key] = 'left' if new_state[key] == 'right' else 'right'

            new_state['farmer'] = 'left' if new_state['farmer'] == 'right' else 'right'

            if (
                    all(value in ['left', 'right'] for value in new_state.values()) and
                    is_valid(new_state) and
                    tuple(new_state.values()) not in visited
            ):
                new_path = path + [new_state]
                queue.append((new_state, new_path))

    return None

solution = bfs()

if solution:
    print("\nSolution found:")
    for i, step in enumerate(solution):
        print(f"Step {i + 1}: {step}")
else:
    print("No solution found.")
