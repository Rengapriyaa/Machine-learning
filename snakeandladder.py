import numpy as np

# Define the snake and ladder board
BOARD_SIZE = 100
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Function to calculate the new position based on dice roll and handle snakes and ladders
def get_new_position(pos, dice_roll):
    new_pos = pos + dice_roll
    if new_pos in snakes:
        print(f"Oops! Bitten by a snake at {new_pos}. Sliding down to {snakes[new_pos]}.")
        return snakes[new_pos]
    elif new_pos in ladders:
        print(f"Great! Climbed a ladder from {new_pos} to {ladders[new_pos]}.")
        return ladders[new_pos]
    elif new_pos > BOARD_SIZE:
        print(f"Rolled too high! Staying at {pos}.")
        return pos  # Stay in the same position if roll exceeds 100
    return new_pos

# Function to simulate the game based on user input
def simulate_game_with_user_input():
    position = 1
    steps = 0
    path = [position]

    print("\nYou are starting the game from position 1. Let's go!")
    
    while position != 100:
        try:
            # Get user input for the dice roll (1-6)
            dice_roll = int(input("Enter dice roll (1-6): "))
            if dice_roll < 1 or dice_roll > 6:
                print("Invalid dice roll! Please enter a number between 1 and 6.")
                continue

            new_position = get_new_position(position, dice_roll)
            path.append(new_position)
            position = new_position
            steps += 1

            print(f"You moved to position {position}.")

        except ValueError:
            print("Invalid input! Please enter a number.")

    return path, steps

# Simulate the game and show the result
path, steps = simulate_game_with_user_input()
print("\nGame Over!")
print("Your Path: ", path)
print("Number of Steps Taken: ", steps)