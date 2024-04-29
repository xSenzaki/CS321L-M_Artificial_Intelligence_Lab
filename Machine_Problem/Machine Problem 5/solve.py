# Araullo, John Art Marie G.							                                     
# BSCS-NS-3A                                                                               
# CS321L-M - Artificial Intelligence                                                                                      
# Machine Problem #5 - Wumpus World Game
# Algorithm: Davis-Putnam Algorithm (Complete Backtracking Algorithm)
# Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The DPLL algorithm is a backtracking-based algorithm used to solve the Boolean satisfiability (SAT) problem.

from world import World

class WumpusWorldSolver:
    def __init__(self, world):
        self.world = world
        self.knowledge_base = []  # Initialize an empty knowledge base

    def perceive(self, percept):
        if percept == "Breeze":
            # Add clauses representing the presence of a pit in adjacent cells
            for i in range(self.world.row):
                for j in range(self.world.col):
                    if self.world.board[i][j].breeze:
                        # Add clauses for the presence of a pit in the adjacent cells
                        clauses = []
                        if i > 0:
                            clauses.append([f"P{i-1},{j}"])
                        if i < self.world.row - 1:
                            clauses.append([f"P{i+1},{j}"])
                        if j > 0:
                            clauses.append([f"P{i},{j-1}"])
                        if j < self.world.col - 1:
                            clauses.append([f"P{i},{j+1}"])
                        self.knowledge_base.extend(clauses)
        elif percept == "Stench":
            # Add clauses representing the presence of the Wumpus in adjacent cells
            for i in range(self.world.row):
                for j in range(self.world.col):
                    if self.world.board[i][j].stench:
                        # Add clauses for the presence of the Wumpus in the adjacent cells
                        clauses = []
                        if i > 0:
                            clauses.append([f"W{i-1},{j}"])
                        if i < self.world.row - 1:
                            clauses.append([f"W{i+1},{j}"])
                        if j > 0:
                            clauses.append([f"W{i},{j-1}"])
                        if j < self.world.col - 1:
                            clauses.append([f"W{i},{j+1}"])
                        self.knowledge_base.extend(clauses)
        elif percept == "Glitter":
            # Add clauses representing the presence of the gold
            for i in range(self.world.row):
                for j in range(self.world.col):
                    if self.world.board[i][j].glitter:
                        self.knowledge_base.append([f"G{i},{j}"])

    # Davis-Putnam-Logemann-Loveland (DPLL) algorithm
    def davis_putnam(self, symbols, model):
        def unit_propagate(clauses, model):
            while True:
                unit_clauses = [c for c in clauses if len(c) == 1]
                if not unit_clauses:
                    break
                p = unit_clauses[0][0]
                model[p] = True
                clauses = [c for c in clauses if p not in c]
            return clauses, model

        def dpll(clauses, symbols, model):
            clauses, model = unit_propagate(clauses, model)
            if not clauses:
                return model
            if any(len(c) == 0 for c in clauses):
                return None  # Unsatisfiable

            p = symbols.pop()
            model_copy = model.copy()
            model_copy[p] = True
            result = dpll([c for c in clauses if p not in c], symbols.copy(), model_copy)
            if result is not None:
                return result

            model[p] = False
            return dpll([c for c in clauses if -p not in c], symbols.copy(), model)

        # Initialize symbols representing different propositions in the world
        symbols = [f"P{i},{j}" for i in range(self.world.row) for j in range(self.world.col)]  # Cells
        symbols.extend([f"W{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Wumpus
        symbols.extend([f"G{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Gold
        symbols.extend([f"B{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Breeze
        symbols.extend([f"S{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Stench

        # Call the DPLL algorithm to solve the Wumpus World problem
        model = {}  # Empty model initially
        result = dpll(self.knowledge_base, symbols, model)
        return result

    def solve(self):
        # Perform perceptions and update the knowledge base
        for percept in self.world.perceptions():
            self.perceive(percept)

        # Initialize symbols representing different propositions in the world
        symbols = [f"P{i},{j}" for i in range(self.world.row) for j in range(self.world.col)]  # Cells
        symbols.extend([f"W{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Wumpus
        symbols.extend([f"G{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Gold
        symbols.extend([f"B{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Breeze
        symbols.extend([f"S{i},{j}" for i in range(self.world.row) for j in range(self.world.col)])  # Stench

        # Call the Davis-Putnam algorithm to solve the Wumpus World problem
        model = {}  # Empty model initially
        result = self.davis_putnam(symbols, model)

        if result is not None:
            # Solution found
            # Extract information from the model and print the solution
            print("Solution found!")
            print("Model:", result)
        else:
            print("No solution found. The Wumpus World is unsolvable.")

def main():
    numOfPits = 3  # Number of pits in the Wumpus World
    world = World(numOfPits)
    world.show()  # Show the generated world
    solver = WumpusWorldSolver(world)
    solver.solve()

if __name__ == "__main__":
    main()
