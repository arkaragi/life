"""
This script provides simulations of the original Game of Life and its variant
Problife using the original, or custom, user-defined rules.

The 'main_original' function is a simple implementation of the Game of Life
using the original rules.
The 'main_problife' function uses a modified version of the Game of Life rules,
referred to as Problife.
The 'main_custom_rules' function allows users to specify their own custom rules
for the Game of Life simulation.
"""

import numpy as np

from life.modules.game import GameOfLife
from life.modules.rule import Rule


def main_original():
    """
    Run the Game of Life simulation using the original variant.

    This function instantiates the GameOfLife class, initializes the grid,
    sets the original rules, and simulates the game.
    """

    # Instantiate the GameOfLife class
    game = GameOfLife(variant="original")

    # Initialize the grid with a grid_size of 10 and 25% cells alive
    game.initialize_grid(grid_size=10,
                         alive_percentage=0.25,
                         seed=None)

    # Visualize the initial grid
    game.visualize_grid()

    # Set the original Game of Life rules
    game.set_rules(original_rules=True)

    # Simulate the game
    game.simulate(max_iter=200,
                  visuals=True)


def main_problife():
    """
    Run the Problife simulation.

    This function instantiates the GameOfLife class, initializes the grid,
    sets a custom grid for testing, sets the original rules but for Problife
    and simulates the game.
    """

    # Instantiate the GameOfLife class
    game = GameOfLife(variant="problife")

    # Initialize the grid with a grid_size of 10 and 25% cells alive
    game.initialize_grid(grid_size=6,
                         alive_percentage=0.25,
                         seed=None)

    # Set a custom grid for testing
    grid = np.array([
        [0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ])
    game.set_custom_grid(grid)

    # Visualize the initial grid
    game.visualize_grid()

    # Set the original Game of Life rules
    game.set_rules(original_rules=True)

    # Simulate the game
    game.simulate(max_iter=10,
                  visuals=True)


def main_custom_rules():
    """
    Run a Game of Life simulation with custom rules.

    This function instantiates the GameOfLife class, initializes the grid,
    sets custom rules for the simulation, and then simulates the game. The
    custom rules can be defined by the user and can be added or modified in
    the 'rules' dictionary.
    """

    # Instantiate the GameOfLife class
    game = GameOfLife(variant="original")

    # Initialize the grid with a grid_size of 10 and 25% cells alive
    game.initialize_grid(grid_size=10,
                         alive_percentage=0.25,
                         seed=2)

    # Visualize the initial grid
    game.visualize_grid()

    # Set custom rules
    rules = {
        0: Rule("s", 2, 1),
        1: Rule("s", 3, 1),
        2: Rule("b", 1, 1),
        3: Rule("b", 3, 1),
    }
    game.set_rules(original_rules=False,
                   rules=rules)

    # Simulate the game
    game.simulate(max_iter=200,
                  visuals=True)


if __name__ == "__main__":

    # Simulate Game of Life
    main_original()

    # Simulate Problife
    # main_problife()

    # Simulate Game of Life with custom rules
    # main_custom_rules()
