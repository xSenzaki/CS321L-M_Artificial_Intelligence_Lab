# +--------------------------------------------------------------------------+
# | Araullo, John Art Marie G.                                               |
# | BSCS-NS-3A                                                               |
# | CS321L-M - Artificial Intelligence                                       |
# | Machine Problem #3                                                       |
# | 4x4 Killer Sudoku Solver with Backjumping Algorithm.                     |
# | Algorithm: Local Beam Search with Backjumping Heuristic                  |
# | The user can input the initial state or generate a random initial state. |
# +--------------------------------------------------------------------------+

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random
import copy

class KillerSudokuSolverUI(QWidget):
    def __init__(self):
        super().__init__()

        # Algorithm Parameters
        self.size = 4
        self.beam_width = 20  
        self.max_iterations = 5000  

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
        # Read Initial State
        initial_state = self.read_table()
        # Run Beam Search Algorithm (With Backjumping Heuristic)
        solution = beam_search(self.size, self.beam_width, self.max_iterations, self.cages, initial_state)

        if solution:
            self.display_solution(solution)
        else:
            self.display_no_solution()

    def generate_initial_state(self):
        # Generate Random Initial State
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
        # Read State
        state = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                item = self.table.item(i, j)
                if item is not None and item.text().isdigit():
                    state[i][j] = int(item.text())
        return state

    def populate_table(self, data):
        # Populate Table
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

# Algorithm 
def beam_search(size, beam_width, max_iterations, cages, initial_state=None):
    current_state = generate_initial_state(size, cages, initial_state)
    current_fitness = calculate_fitness(current_state, cages)
    current_cost = 0

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_state, beam_width, cages)

        best_neighbor = max(neighbors, key=lambda x: calculate_fitness(x, cages))
        best_neighbor_fitness = calculate_fitness(best_neighbor, cages)

        if best_neighbor_fitness == size * 2 + len(cages):
            return best_neighbor  # Solution found

        if best_neighbor_fitness <= current_fitness:
            current_state = best_neighbor
            current_fitness = best_neighbor_fitness
        else:
            # Apply Backjumping Heuristic
            if random.random() < acceptance_probability(current_fitness, best_neighbor_fitness, current_cost):
                current_state = best_neighbor
                current_fitness = best_neighbor_fitness
            else:
                current_cost += 1

    return None  # Solution not found

# Calculate fitness of a Sudoku state based on rows, columns, and cages
def calculate_fitness(state, cages):
    fitness = 0

    # Check rows
    for row in state:
        if len(set(row)) == len(row):
            fitness += 1

    # Check columns
    for col in range(len(state[0])):
        column_values = [state[row][col] for row in range(len(state))]
        if len(set(column_values)) == len(column_values):
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

# Generate neighbors for the beam search algorithm
def generate_neighbors(current_state, num_neighbors, cages):
    neighbors = []
    for _ in range(num_neighbors):
        new_state = copy.deepcopy(current_state)
        # Generate a neighbor by swapping two random cell values within the same region
        i, j = random.randint(0, len(current_state) - 1), random.randint(0, len(current_state) - 1)
        x, y = random.randint(0, len(current_state) - 1), random.randint(0, len(current_state) - 1)

        region_i, region_j = i // int(len(current_state) ** 0.5), j // int(len(current_state) ** 0.5)
        region_x, region_y = x // int(len(current_state) ** 0.5), y // int(len(current_state) ** 0.5)

        if region_i == region_x and region_j == region_y:
            new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
            neighbors.append(new_state)
        else:
            neighbors.append(generate_neighbors(current_state, 1, cages)[0])  # Retry to ensure same region
    return neighbors

# Calculate acceptance probability for the beam search algorithm
def acceptance_probability(current_fitness, neighbor_fitness, current_cost):
    return 1 / (1 + (neighbor_fitness - current_fitness) * (1 + current_cost))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KillerSudokuSolverUI()
    window.show()
    sys.exit(app.exec_())
