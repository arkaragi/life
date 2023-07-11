"""
This module provides an implementation of the Cell class, which is the basic
building block for representing the grid of a cellular automaton, such as the
Game of Life and its variants.

The Cell class is designed to accommodate different types of cellular automaton
games. For the deterministic Game of Life, a Cell holds a binary state which is
either alive (1) or dead (0), and evolves according to specific set rules based
on its own and neighboring cells' states. For a probabilistic variant, known as
Problife, the Cell carries a state value that ranges continuously from 0 to 1,
representing the probability of the cell being alive. Its evolution is driven by
a combination of deterministic rules and probabilistic factors.
"""

import itertools
import math
from typing import Union

import numpy as np

from life.modules.rule import Rule


class Cell:
    """
    A class representing a cell inside the grid of the Game of Life or its
    probabilistic variant, Problife.

    The `Cell` class offers functionalities to update the cell's state and
    keep track of its live neighbors. Each cell's position is denoted by
    its row and column coordinates within the grid, and its state signifies
    its life status.

    In the classic Game of Life, the state is a binary value: 1 represents
    a live cell, and 0 represents a dead cell. In Problife, the state is a
    real number within the range [0, 1], expressing the probability of the
    cell is alive at that time.

    Parameters
    ----------
    row: int
        The row coordinate of the cell within the grid.

    col: int
        The column coordinate of the cell within the grid.

    state: int | float
        The current state of the cell.
        In the classic Game of Life, this attribute holds a binary value, with
        0 represents a dead cell, and 1 represents a live cell.
        In Problife, it is a real number within [0, 1] range, representing the
        probability of the cell staying alive in the upcoming generation.
    """

    def __init__(self,
                 row: int,
                 col: int,
                 state: Union[int, float]):
        if not isinstance(row, int) or row < 0:
            raise ValueError("Row must be a non-negative integer")
        if not isinstance(col, int) or col < 0:
            raise ValueError("Column must be a non-negative integer")
        if not isinstance(state, (int, float)) and not 0 <= state <= 1:
            raise ValueError("State must be a float between 0 and 1 (inclusive)")
        self.row = row
        self.col = col
        self.state = state

    def __str__(self):
        return f"Cell({self.row}, {self.col}, {self.state})"

    def __repr__(self):
        return f"Cell(row={self.row}, col={self.col}, state={self.state})"

    def __call__(self):
        return self.state

    def calculate_alive_neighbors(self,
                                  n_neighbors: int,
                                  neighboring_cells: list):
        """
        Calculate the total probability of a cell having exactly 'n' alive
        neighbors.

        This method computes the total probability of a cell having exactly
        'n' alive neighbors by iterating over all possible combinations of
        'n' neighbors. For each combination, it calculates the product of
        the probabilities that the selected neighbors are alive and that the
        remaining neighbors are dead. These individual probabilities for each
        combination are then added together to obtain the total probability.

        Parameters
        ----------
        n_neighbors: int
            The number of alive neighbors to consider.
            Should be an integer between 0 and 8 (inclusive).

        neighboring_cells: list
            A list of neighboring cells represented by Cell objects.

        Returns
        -------
        cell_alive_prob: float
            The total probability of the cell having exactly 'n' alive neighbors.
            This is a float value in the range of [0, 1].
        """

        # Total alive probability for current cell
        cell_alive_prob = 0.0

        # Pre-calculate the products of all neighboring cell states and their complements
        products = [cell.state for cell in neighboring_cells]
        complements = [1 - p for p in products]

        # Loop over all combinations of n neighbors
        for combination in itertools.combinations(range(len(neighboring_cells)), n_neighbors):
            # Calculate the probability of this combination being alive
            alive_prob = math.prod(products[i] for i in combination)

            # Calculate the probability of the other cells being dead
            dead_prob = math.prod(complements[i] for i in range(len(neighboring_cells))
                                  if i not in combination)

            # Add the probability of this combination to the total probability
            cell_alive_prob += alive_prob * dead_prob

        return cell_alive_prob

    def update_state(self,
                     neighboring_cells: list):
        """
        Update the state of the cell.

        This method calculates the new state of the cell based on the rules
        defined for survival and birth. For each possible number of neighbors
        (0 to 8 inclusive), it calculates the contribution to the new state.
        The contribution depends on the survival and birth probabilities for
        that number of neighbors and the probability of the cell having that
        many neighbors alive.

        Parameters
        ----------
        neighboring_cells: list
            A list of neighboring cells represented by Cell objects.

        Returns
        -------
        new_state: float
            The updated state of the cell with a value between 0 and 1.
            This value is rounded to two decimal places. It represents
            the probability of the cell being alive in the next generation.
        """

        # Retrieve the rules for survival and birth conditions
        rules_by_neighbors = Rule.get_rules_by_neighbors()

        # Define the new state of the cell
        new_state = 0

        # Iterate over all possible number of neighbors (0 to 8 inclusive)
        for n_neighbors in range(9):
            # If there are rules defined for the current number of neighbors
            if n_neighbors in list(rules_by_neighbors.keys()):
                # Calculate the total probability of exactly n neighbors being alive
                Nt = self.calculate_alive_neighbors(n_neighbors, neighboring_cells)

                # Iterate over the rules defined for the current number of neighbors
                s_term, b_term = 0, 0
                for rule in rules_by_neighbors[n_neighbors]:
                    # If it's a survival rule, calculate the survival term
                    if rule.condition == "s":
                        s_term = rule.probability * self.state
                    # If it's a birth rule, calculate the birth term
                    if rule.condition == "b":
                        b_term = rule.probability * (1 - self.state)

                # Add the contribution of the current number of neighbors to the new state
                new_state += Nt * (s_term + b_term)

        # Return the new state, rounded to 2 decimal places
        return np.round(new_state, 2)
