# Araullo, John Art Marie G.							                                     
# BSCS-NS-3A                                                                               
# CS321L-M - Artificial Intelligence                                                                                      
# Machine Problem #5 - Wumpus World Game
# Algorithm: Davis-Putnam Algorithm (Complete Backtracking Algorithm)
# Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The DPLL algorithm is a backtracking-based algorithm used to solve the Boolean satisfiability (SAT) problem.

import random
from percept import Percept

class World:
    def __init__(self, numOfPits):
        # Initialize the size of the world grid
        self.row = 4
        self.col = 4
        # Create a 2D grid of Percept objects representing the world
        self.board = [[Percept() for j in range(self.col)] for i in range(self.row)]

        self.addPits(numOfPits)
        self.addWumpus()
        self.addGold()

    # Generate the world by adding pits, wumpus, and gold
    def perceptions(self):
        perceptions = []
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j].breeze:
                    perceptions.append("Breeze")
                if self.board[i][j].stench:
                    perceptions.append("Stench")
                if self.board[i][j].glitter:
                    perceptions.append("Glitter")
        return perceptions

    # Add pits randomly to the world
    def addPits(self, numOfPits):
        i = 0
        while i < numOfPits:
            rr = random.randint(0, self.row - 1)
            rc = random.randint(0, self.col - 1)
            if (rr != 0 and rc != 0) and not self.board[rr][rc].pit and not self.board[rr][rc].wumpus and not self.board[rr][rc].gold:
                self.board[rr][rc].pit = True
                self.addBreeze(rr, rc)
                i += 1

    # Add the Wumpus to the world
    def addWumpus(self):
        while True:
            rr = random.randint(0, self.row - 1)
            rc = random.randint(0, self.col - 1)
            if self.board[rr][rc].pit or (rr == 0 and rc == 0):
                continue
            else:
                self.board[rr][rc].wumpus = True
                self.addStench(rr, rc)
                break

    # Add the gold to the world
    def addGold(self):
        while True:
            rr = random.randint(0, self.row - 1)
            rc = random.randint(0, self.col - 1)

            if (self.board[rr][rc].pit or self.board[rr][rc].wumpus or (rr == 0 and rc == 0)):
                continue
            else:
                self.board[rr][rc].gold = True
                self.addGlitter(rr, rc)
                break

    # Helper method to add breeze to adjacent cells
    def addBreeze(self, rr, rc):
        if (rr - 1 >= 0):
            self.board[rr - 1][rc].breeze = True
        if (rr + 1 < self.row):
            self.board[rr + 1][rc].breeze = True
        if (rc - 1 >= 0):
            self.board[rr][rc - 1].breeze = True
        if (rc + 1 < self.col):
            self.board[rr][rc + 1].breeze = True

    # Helper method to add stench to adjacent cells
    def addStench(self, rr, rc):
        if (rr - 1 >= 0):
            self.board[rr - 1][rc].stench = True
        if (rr + 1 < self.row):
            self.board[rr + 1][rc].stench = True
        if (rc - 1 >= 0):
            self.board[rr][rc - 1].stench = True
        if (rc + 1 < self.col):
            self.board[rr][rc + 1].stench = True

    # Helper method to add glitter to adjacent cells
    def addGlitter(self, rr, rc):
        if (rr - 1 >= 0):
            self.board[rr - 1][rc].glitter = True
        if (rr + 1 < self.row):
            self.board[rr + 1][rc].glitter = True
        if (rc - 1 >= 0):
            self.board[rr][rc - 1].glitter = True
        if (rc + 1 < self.col):
            self.board[rr][rc + 1].glitter = True

    # Display the world grid
    def show(self):
        board = [None] * 4
        for r in range(self.row):
            board[r] = [None] * 4
            for c in range(self.col):
                if self.board[r][c].gold:
                    board[r][c] = "G"
                elif self.board[r][c].wumpus:
                    board[r][c] = "W"
                elif self.board[r][c].pit:
                    board[r][c] = "P"
                else:
                    board[r][c] = "xx"
        for r in range(4):
            print(board[r])
