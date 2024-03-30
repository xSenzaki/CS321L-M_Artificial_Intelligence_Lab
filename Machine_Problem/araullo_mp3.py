# Araullo, John Art Marie G.
# BSCS-NS-3A
# CS321L-M - Artificial Intelligence
# Machine Problem #3
# 4x4 Killer Sudoku Solver with Backjumping Algorithm.
# The user can input the initial state or generate a random initial state.

import sys
import random
import copy

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class KillerSudokuSolverUI(QWidget):
    def __init__(self):
        super().__init__()

        self.size = 4
        self.beam_width = 5
        self.max_iterations = 1000

        # Define the initial cages
        self.cages = [
            {'start': (0, 0), 'end': (1, 1), 'sum': 5},
            {'start': (0, 2), 'end': (1, 3), 'sum': 6},
            {'start': (2, 0), 'end': (3, 1), 'sum': 7},
            {'start': (2, 2), 'end': (3, 3), 'sum': 8}
        ]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Killer Sudoku Solver')
        self.setGeometry(100, 100, 400, 400)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.table = QTableWidget(self)
        self.table.setRowCount(self.size)
        self.table.setColumnCount(self.size)

        for i in range(self.size):
            for j in range(self.size):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

        solve_button = QPushButton('Solve', self)
        solve_button.clicked.connect(self.solve_sudoku)

        generate_button = QPushButton('Generate Initial State', self)
        generate_button.clicked.connect(self.generate_initial_state)

        layout = QVBoxLayout()
        layout.addWidget(self.result_label)
        layout.addWidget(self.table)
        layout.addWidget(solve_button)
        layout.addWidget(generate_button)

        self.setLayout(layout)

    def solve_sudoku(self):
        initial_state = self.read_table()

        solution, steps = beam_search(self.size, self.beam_width, self.max_iterations, self.cages, initial_state)

        if solution:
            self.display_solution(solution)
        else:
            solution, steps = backjumping_search(self.size, self.cages, initial_state)
            if solution:
                self.display_solution(solution)
            else:
                self.display_no_solution()

        print("Step-by-step Solution:")
        prev_state = None
        for idx, step in enumerate(steps):
            if step != prev_state:
                print(f"State {idx + 1}:")
                print_sudoku(step)
                print()
            prev_state = step

    def generate_initial_state(self):
        initial_state = generate_initial_state(self.size, self.cages)

        self.populate_table(initial_state)

    def display_solution(self, solution):
        self.result_label.setText("Solution found:")
        self.result_label.setFont(QFont("Arial", 12, QFont.Bold))

        self.populate_table(solution)

    def display_no_solution(self):
        self.result_label.setText("Solution not found.")
        self.result_label.setFont(QFont("Arial", 12, QFont.Bold))

    def read_table(self):
        state = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                item = self.table.item(i, j)
                if item is not None and item.text().isdigit():
                    state[i][j] = int(item.text())
        return state

    def populate_table(self, data):
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = self.table.item(i, j)
                if item is not None:
                    item.setText(str(value))

# Generate a random initial state
def generate_initial_state(size, cages, initial_state=None):    
    if initial_state is not None:
        return initial_state
    state = [[0] * size for _ in range(size)]
    for cage in cages:
        values = list(range(1, size + 1))
        random.shuffle(values)
        for i in range(cage['start'][0], cage['end'][0] + 1):
            for j in range(cage['start'][1], cage['end'][1] + 1):
                state[i][j] = values.pop()
    return state

def backjumping_search(size, cages, initial_state):
    def is_valid_move(state, row, col, num):
        # Check row and column
        if num in state[row] or num in [state[i][col] for i in range(size)]:
            return False

        # Check region (cage)
        for cage in cages:
            if row in range(cage['start'][0], cage['end'][0] + 1) and col in range(cage['start'][1], cage['end'][1] + 1):
                region_values = [state[i][j] for i in range(cage['start'][0], cage['end'][0] + 1) for j in range(cage['start'][1], cage['end'][1] + 1)]
                if num in region_values:
                    return False

        return True

    def solve(state):
        for row in range(size):
            for col in range(size):
                if state[row][col] == 0:
                    for num in range(1, size + 1):
                        if is_valid_move(state, row, col, num):
                            state[row][col] = num
                            if solve(state):
                                return True
                            state[row][col] = 0  # Backjump
                    return False  # No valid move

        return True

    solved_state = copy.deepcopy(initial_state)
    if solve(solved_state):
        return solved_state, []  
    else:
        return None, []  

def beam_search(size, beam_width, max_iterations, cages, initial_state=None):
    current_state = generate_initial_state(size, cages, initial_state)
    current_fitness = calculate_fitness(current_state, cages)
    steps = [copy.deepcopy(current_state)]  # Store initial state

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_state, beam_width, cages)

        best_neighbor = max(neighbors, key=lambda x: calculate_fitness(x, cages))
        best_neighbor_fitness = calculate_fitness(best_neighbor, cages)

        if best_neighbor_fitness == size * 2 + len(cages):
            steps.append(best_neighbor)
            return best_neighbor, steps  # Solution found

        current_state = best_neighbor
        steps.append(best_neighbor)
        current_fitness = best_neighbor_fitness

    return None, steps  # Solution not found

def calculate_fitness(state, cages):
    fitness = 0

    # Check rows and columns
    for i in range(len(state)):
        if len(set(state[i])) == len(state[i]):
            fitness += 1
        if len(set(state[j][i] for j in range(len(state)))) == len(state):
            fitness += 1

    # Check regions (cages)
    for cage in cages:
        region_values = []
        for i in range(cage['start'][0], cage['end'][0] + 1):
            for j in range(cage['start'][1], cage['end'][1] + 1):
                region_values.append(state[i][j])

        # Check if the region has all required values
        if set(range(1, len(state) + 1)) == set(region_values):
            fitness += 1

    return fitness

def generate_neighbors(current_state, num_neighbors, cages):
    neighbors = []
    for _ in range(num_neighbors):
        i, j = random.randint(0, len(current_state) - 1), random.randint(0, len(current_state) - 1)
        new_state = copy.deepcopy(current_state)
        new_state[i][j] = random.choice(list(set(range(1, len(current_state) + 1)) - {current_state[i][j]}))
        neighbors.append(new_state)
    return neighbors

def print_sudoku(sudoku):
    for row in sudoku:
        print(" ".join(map(str, row)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KillerSudokuSolverUI()
    window.show()
    sys.exit(app.exec_())
