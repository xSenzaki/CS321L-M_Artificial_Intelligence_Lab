# Machine Problem #5
    Algorithm: Davis-Putnam Algorithm (Complete Backtracking Algorithm)
    Davis-Putnam-Logemann-Loveland (DPLL) algorithm. The DPLL algorithm is a backtracking-based algorithm used to solve the Boolean satisfiability (SAT) problem. 
    Wumpus World Game

# CONSOLE-BASED WUMPUS WORLD GAME SOLVER
    This program solves the ai puzzle of the Wumpus World game using the Davis-Putnam Algorithm (DPLL). In order to find the gold while avoiding the dangers an AI agent must navigate a grid-based landscape full with obstacles including pits and a dangerous Wumpus.

    Please do take note that the world is represented as a 4x4 grid.

# GAMEPLAY
    P - Pit (Dangerous, avoid falling into pits)
    W - Wumpus (Dangerous, avoid encountering the Wumpus)
    G - Gold (Your objective is to find and collect the gold)
    xx - Empty cell

    Breeze - Indicates nearby pits
    Stench - Indicates the presence of the Wumpus nearby
    Glitter - Indicates the presence of gold in the current cell

    Perceptions:
    As the AI agent moves through the world, it receives sensory information (perceptions) like breeze, stench, and glitter, which provide clues about nearby hazards and the presence of gold.

    Moves:
    The AI agent can move up, down, left, or right within the grid, making decisions based on its perceptions.

# OBJECTIVE
    Find the gold and return to the starting position without falling into pits or encountering the Wumpus.

# GRID DISPLAY
    ['xx', 'xx', 'xx', 'xx']
    ['xx', 'xx', 'xx', 'P']
    ['xx', 'P', 'G', 'xx']
    ['xx', 'xx', 'P', 'W']

# AI-AGENT ENVIRONMENT
    1. The program generates a random world layout with pits, the Wumpus, gold, and empty cells.
    2. The AI agent detects its environment as it travels through the world and updates its knowledge base accordingly.
    3. The AI agent has a knowledge base of clauses representing world propositions such as pits, the Wumpus, gold, breeze, stench. Symbols are used to represent these propositions, with each symbol corresponding to a specific cell or element in the grid.
    4. Davis-Putnam Algorithm (DPLL) Implementation. A backtracking-based approach used to determine the satisfiability of logical formulas. The solver applies DPLL to the knowledge base, aiming to find a model (assignment of truth values to symbols) that satisfies all clauses.
    5. If a satisfying model is found, the solver concludes that a solution exists and provides the model as the solution. If no satisfying model is found, the solver determines that the Wumpus World configuration is unsolvable given the current perceptions and knowledge.
