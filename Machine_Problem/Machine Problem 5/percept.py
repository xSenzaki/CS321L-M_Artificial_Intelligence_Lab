# Araullo, John Art Marie G.							                                     
# BSCS-NS-3A                                                                               
# CS321L-M - Artificial Intelligence                                                                                      
# Machine Problem #5 - Wumpus World Game
# Algorithm: Davis-Putnam Algorithm (Complete Backtracking Algorithm)
# Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The DPLL algorithm is a backtracking-based algorithm used to solve the Boolean satisfiability (SAT) problem.

class Percept:
    def __init__(self):
        # Initialize percept attributes
        self.wumpus = False
        self.pit = False
        self.gold = False
        self.stench = False
        self.breeze = False
        self.glitter = False
        self.visited = False

        # Initialize values used in the Davis-Putnam-Logemann-Loveland (DPLL) algorithm
        self.pitValue = 0
        self.wumpusValue = 0
        self.visitedValue = 0
