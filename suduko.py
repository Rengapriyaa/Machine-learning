import numpy as np
import random

# Create a simple Sudoku environment
class SudokuEnvironment:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.initial_grid = self.grid.copy()
        self.size = 9
        self.empty_cells = self.get_empty_cells()
    
    def get_empty_cells(self):
        """Identify all empty cells in the Sudoku grid."""
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r, c] == 0]
    
    def is_valid_move(self, row, col, num):
        """Check if placing 'num' in (row, col) is valid."""
        # Check the row
        if num in self.grid[row, :]:
            return False
        # Check the column
        if num in self.grid[:, col]:
            return False
        # Check the 3x3 subgrid
        sub_row, sub_col = row // 3 * 3, col // 3 * 3
        if num in self.grid[sub_row:sub_row + 3, sub_col:sub_col + 3]:
            return False
        return True
    
    def reset(self):
        """Reset the Sudoku grid to the initial state."""
        self.grid = self.initial_grid.copy()
        self.empty_cells = self.get_empty_cells()
    
    def step(self, row, col, num):
        """Place a number in a cell and return reward and status."""
        if self.is_valid_move(row, col, num):
            self.grid[row, col] = num
            self.empty_cells.remove((row, col))
            if len(self.empty_cells) == 0:
                return 1, True  # Return reward and game completion
            return 1, False  # Valid move, game not finished
        else:
            return -1, False  # Invalid move, game not finished
    
    def is_complete(self):
        """Check if the Sudoku grid is fully filled and correct."""
        return len(self.empty_cells) == 0

# Q-Learning for Sudoku
class SudokuQAgent:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1, episodes=10000):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.episodes = episodes
        # Initialize Q-table for each empty cell and number (1-9)
        self.q_table = np.zeros((env.size, env.size, 9))

    def train(self):
        for episode in range(self.episodes):
            self.env.reset()
            state = self.env.grid.copy()
            done = False
            
            while not done:
                # Choose a random empty cell
                row, col = random.choice(self.env.empty_cells)
                
                # Choose action: 1-9 for this cell (either explore or exploit)
                if np.random.rand() < self.epsilon:
                    num = np.random.randint(1, 10)  # Exploration
                else:
                    num = np.argmax(self.q_table[row, col]) + 1  # Exploitation
                
                # Take action
                reward, done = self.env.step(row, col, num)
                
                # Q-Learning update
                if not done:
                    next_state = self.env.grid.copy()
                    future_reward = np.max(self.q_table[row, col])  # Max future reward
                else:
                    future_reward = 0
                
                # Update Q-value
                self.q_table[row, col, num - 1] += self.alpha * (reward + self.gamma * future_reward - self.q_table[row, col, num - 1])
    
    def solve(self):
        """Solve the Sudoku puzzle using learned Q-table."""
        self.env.reset()
        path = []
        while not self.env.is_complete():
            row, col = random.choice(self.env.empty_cells)
            num = np.argmax(self.q_table[row, col]) + 1
            _, _ = self.env.step(row, col, num)
            path.append((row, col, num))
        return self.env.grid, path

# Get user input for Sudoku grid
def get_user_sudoku_input():
    print("Enter the Sudoku puzzle row by row (use 0 for empty cells):")
    grid = []
    for i in range(9):
        row = input(f"Row {i + 1}: ")
        grid.append([int(x) for x in row.split()])
    return grid

# Main function to run the RL Sudoku Solver
def main():
    # Get user input for the Sudoku grid
    user_grid = get_user_sudoku_input()
    
    # Initialize the environment
    env = SudokuEnvironment(user_grid)
    
    # Initialize the Q-learning agent
    agent = SudokuQAgent(env)
    
    # Train the agent
    print("Training the agent...")
    agent.train()
    
    # Solve the Sudoku
    solved_grid, path = agent.solve()
    
    # Print the solved grid
    print("\nSolved Sudoku Grid:")
    print(solved_grid)
    print("\nPath of moves:")
    for move in path:
        print(f"Row: {move[0] + 1}, Col: {move[1] + 1}, Number: {move[2]}")

if __name__ == "__main__":
    main()