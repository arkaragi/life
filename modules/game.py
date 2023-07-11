"""
This module provides an implementation of the Game of Life cellular automaton
and its variant Problife.

The Game of Life is a cellular automaton devised by the British mathematician
John Horton Conway in 1970. It is a zero-player game, such that its evolution
is determined by its initial state, requiring no further input. It consists
of a grid of cells that evolve over discrete time steps according to a set of
predefined rules. Each cell in the grid has two states, alive or dead, and is
occupying a specific location. The state of a cell at the next generation is
determined by its current state and the states of its neighbors, according to
the rules of the game.

Problife is a variant of the Game of Life, where the states of the cells are
not represented by a binary, but by a real number in the range [0, 1]. This
state at a given time step represents the probability that the cell is alive
at that time step. The evolution of a cell in ProbLife is defined by a set
of rules that denote the probability of a cell surviving or being born given
its exact number of living neighbours.

By creating various initial configurations and applying the original or custom
rules, users can explore and observe the dynamic patterns and behaviors that
emerge within the Game of Life cellular automaton and its variant Problife.
"""

import copy

import numpy as np

from life.modules.cell import Cell
from life.modules.rule import Rule


class GameOfLife:
    """
    The GameOfLife class represents a cellular automaton grid and provides
    functionality to simulate the Game of Life or Problife.

    Parameters
    ----------
    variant: str, default="original"
        The variant of the Game of Life to simulate ("original" or "problife").
        By default, it is set to "original".

    Attributes
    ----------
    grid_size: int
        The size of the square grid.

    alive_percentage: float
        The percentage of cells that are initially alive.

    grid: np.array
        The cellular automaton grid, represented as a 2D numpy array of Cell
        objects.

    initial_grid: np.array
        The state of the grid at the initial generation.

    previous_grid: np.array
        The state of the grid from the previous generation.

    rules: dict
        The rules that determine the transitions, stored as a dictionary
        mapping from integers to Rule objects.

    time_step: int
        The current time step of the simulation.
    """

    def __init__(self,
                 variant: str = "original"):
        self.variant = variant

        # Initialize instance attributes to None as default.
        self.grid_size = None
        self.alive_percentage = None
        self.grid = None
        self.initial_grid = None
        self.previous_grid = None
        self.rules = None
        self.time_step = 0

    def count_live_neighbors(self,
                             cell: Cell):
        """
        Count the number of live neighbors around a given cell.

        In the Game of Life, each cell has eight neighbors, which are the cells
        that are horizontally, vertically, or diagonally adjacent. This method
        counts how many of those neighbors are alive.

        Parameters
        ----------
        cell: Cell
            The cell for which live neighbors need to be counted.

        Returns
        -------
        live_neighbor_count: int
            Number of live neighbors.
        """

        # Initialize the live_neighbor_count to 0
        live_neighbor_count = 0

        # Define the offsets representing the positions of the eight
        # neighboring cells.
        offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2)
                   if not i == j == 0]

        # Iterate through the possible neighbor offsets
        for delta_i, delta_j in offsets:
            # Calculate the indices of the neighbor cell
            neighbor_i = (cell.row + delta_i) % self.grid_size
            neighbor_j = (cell.col + delta_j) % self.grid_size
            # Add the state of the neighbor cell to the live_neighbor_count
            live_neighbor_count += self.grid[neighbor_i][neighbor_j].state

        return live_neighbor_count

    def get_neighboring_cells(self,
                              cell: Cell):
        """
        Return the neighboring cells of a given cell.

        This method returns the eight cells that surround a given cell in the
        grid, taking into account the toroidal configuration.
        The returned cells are those that are horizontally, vertically, or
        diagonally adjacent to the input cell.

        Parameters
        ----------
        cell: Cell
            The cell for which neighbors need to be found.

        Returns
        -------
        neighboring_cells: list
            A list that contains the neighboring cells.
        """

        # Initialize the list for neighboring cells
        neighboring_cells = []

        # Define the offsets representing the positions of the eight
        # neighboring cells.
        offsets = [(i, j) for i in range(-1, 2) for j in range(-1, 2)
                   if not i == j == 0]

        # Iterate through the possible neighbor offsets
        for delta_i, delta_j in offsets:
            # Calculate the indices of the neighbor cell
            neighbor_i = (cell.row + delta_i) % self.grid_size
            neighbor_j = (cell.col + delta_j) % self.grid_size
            # Append the neighbor cell to the list
            neighboring_cells.append(self.grid[neighbor_i][neighbor_j])

        return neighboring_cells

    def grid_to_array(self,
                      grid: np.ndarray):
        """
        Converts a grid of cells to a numpy array with elements representing
        the state of the corresponding cell at each position.

        This method expects a grid as input where each element is an object
        of the 'Cell' class. It then reads the state of each cell, creates
        and returns a 2D numpy array.

        Parameters
        ----------
        grid: np.ndarray
            The grid to convert to a numpy array.
            Each element of the grid should be a 'Cell' object.

        Returns
        -------
        np_grid: np.ndarray
            A numpy array representing the grid. Each element of the array
            represents the state of the corresponding cell in the input grid.
        """

        # Convert the grid to a numpy array by iterating over each row and
        # each cell in the row and extracting the 'state' of each cell.
        np_grid = np.array([[cell.state for cell in row] for row in grid])

        return np_grid

    def initialize_grid(self,
                        grid_size: int = 10,
                        alive_percentage: float = 0.2,
                        seed: int | None = None):
        """
        Initializes the grid with a randomized distribution of live and dead
        cells.

        This method creates a two-dimensional numpy array of Cell objects to
        represent the grid. The state of each cell is initially determined
        randomly, based on the `alive_percentage` parameter. This proportion
        dictates the likelihood that a cell will start in the "alive" state.
        If a seed is provided, it is used to initialize the random number
        generator to ensure that the random distribution of live cells is
        reproducible.

        Parameters
        ----------
        grid_size: int
            The size of the grid to be initialized. The grid will be square,
            with both dimensions equal to this size.

        alive_percentage: float
            The proportion of cells that will be initially alive. This should
            be a float in the range [0, 1], where 0 means no cells start alive
            and 1 means all cells start alive.

        seed: int | None, default=None
            A seed for the random number generator, to allow for reproducibility
            of the initial grid state. If not provided, the grid will be
            initialized with a different random state each time this method is
            called.
        """

        # Validate input parameters
        assert isinstance(grid_size, int) and grid_size > 1, \
            "grid_size must be an integer greater than 1."

        # Check if alive_percentage is a float between 0 and 1
        assert isinstance(alive_percentage, float) and 0 <= alive_percentage <= 1, \
            "alive_percentage must be a float in the range [0, 1]."

        # Check if seed is an integer or None
        assert isinstance(seed, (int | None)), "seed must be an float or None.."

        # Set the grid_size and alive_percentage attributes
        self.grid_size = grid_size
        self.alive_percentage = alive_percentage

        # Set the seed for the RNG
        np.random.seed(seed)

        # Set the initial state of the grid
        initial_states = np.random.choice([0, 1],
                                          size=(grid_size, grid_size),
                                          p=[1 - alive_percentage, alive_percentage])

        # Initialize a grid of Cell objects based on the initial_states
        grid = [[Cell(i, j, state) for j, state in enumerate(row)]
                for i, row in enumerate(initial_states)]

        # Convert the grid to a numpy array and set it as the grid attribute
        self.grid = np.array(grid)

        # Keep a copy of the initial grid
        self.initial_grid = copy.deepcopy(self.grid)

    def is_life_extinct(self):
        """
        Checks if all cells are in the dead state.

        Returns
        -------
        extinction_reached: bool
            True if all cells are dead, False otherwise.
        """

        # Convert the grid to a numpy array
        np_grid = self.grid_to_array(self.grid)

        # Check if all cells are dead
        extinction_reached = np.all(np_grid == 0)

        return extinction_reached

    def is_life_stable(self):
        """
        Checks if the state of the grid has not changed from the previous
        time step.

        Returns
        -------
        equilibrium_reached: bool
            True if the grid state is unchanged, False otherwise.
        """

        # Convert the grids to numpy arrays
        curr_grid = self.grid_to_array(self.grid)
        prev_grid = self.grid_to_array(self.previous_grid)

        # Check if the grid state is unchanged
        equilibrium_reached = np.array_equal(curr_grid, prev_grid)

        return equilibrium_reached

    def reset_grid(self):
        """
        Clean the grid by setting all elements to zero.

        This function will set all elements in the 'grid' and 'previous_grid'
        attributes to zero, effectively clearing all living cells and resetting
        the simulation to an initial blank state.
        """

        # Convert every cell in the grid to 0
        for row in self.grid:
            for cell in row:
                cell.state = 0

        self.previous_grid = None

    def set_rules(self,
                  original_rules: bool = True,
                  rules: dict = None):
        """
        Define the rules that govern the evolution of the cellular automaton.

        This method allows users to choose between the original rules of the
        Game of Life or custom rules that they define. These rules determine
        how cells will transition between states in each generation.

        Parameters
        ----------
        original_rules : bool, default=True
            If True, the original rules of the Game of Life will be implemented.
            These rules are:
                1. Any live cell with two or three live neighbors survives.
                2. Any dead cell with three live neighbors becomes a live cell.
            If False, the user must define custom rules and pass them through the
            `rules` parameter.

        rules : dict, default=None
            A dictionary mapping an integer to a Rule object. The integer key
            represents the number of live neighbors a cell has, and the Rule object
            specifies how a cell with that number of live neighbors should transition.
            This parameter is ignored if `original_rules` is True.
        """

        # If original_rules is True
        if original_rules:
            # Set the original rules of the Game of Life
            if self.variant == "original":
                self.rules = Rule.get_original_rules()
            # Set the original rules of Problife
            elif self.variant == "problife":
                self.rules = Rule.get_problife_rules()

        # If original_rules is False, set the custom rules provided by the user
        else:
            # Ensure that the user has provided custom rules
            if rules is None:
                raise ValueError("If original_rules is False, custom rules must be provided.")
            self.rules = rules
            Rule.rules = rules

    def set_custom_grid(self,
                        new_grid: np.ndarray):
        """
        Set the grid to a user-defined state.

        This method updates the state of the game's grid to a user-defined state
        provided in the form of a 2D numpy array. The dimensions of the new_grid
        should match the grid_size used in the initialization of the game.

        Parameters
        ----------
        new_grid : np.ndarray
            A 2D numpy array representing the desired state of the game's grid.
            Each cell should be either 0 (representing a dead cell) or 1
            (representing a live cell).
        """

        assert new_grid.shape == (self.grid_size, self.grid_size), \
            "The shape of new_grid should match the initialized grid size."

        # Update the state of each cell in the grid
        for i, row in enumerate(new_grid):
            for j, value in enumerate(row):
                self.grid[i][j].state = value

    def simulate(self,
                 max_iter: int | None = 100,
                 visuals: bool = True):
        """
        Simulate the evolution of the Game of Life grid for a maximum number
        of iterations or until an equilibrium or extinction is reached.

        This method iteratively updates the state of the grid based on the
        rules of the Game of Life. After each update, it checks for three
        possible termination conditions:

        1. Extinction: All cells on the grid are dead.
        2. Equilibrium: The state of the grid has not changed between iterations.
        3. Max Iterations: The number of iterations has reached `max_iter`.

        Parameters
        ----------
        max_iter : int | None, default=100
            The maximum number of iterations to simulate. If None, the simulation
            continues indefinitely until either extinction or equilibrium is reached.

        visuals : bool, default=True
            If True, the state of the grid is displayed after each iteration.
            This allows for visual tracking of the evolution of the grid over time.
        """

        while True:
            # Update the grid state and increment the iteration counter
            self.update_grid()

            # If visuals is True, print the current state of the grid
            if visuals:
                self.visualize_grid()

            # If extinction is reached, return
            if self.is_life_extinct():
                print(f"Extinction reached after {self.time_step} iterations.\nAborting...")
                return

            # If equilibrium is reached, return
            if self.is_life_stable():
                print(f"Equilibrium reached after {self.time_step} iterations.\nAborting...")
                return

            # If the maximum number of iterations has been reached, abort the simulation
            if max_iter and self.time_step == max_iter:
                print("Maximum number of iterations reached.\nAborting...")
                return

    def step_backwards(self):
        """
        Goes the game's state by one time step, updating all cell states
        in the process.
        """

        # Store a copy of the current grid for future reference
        self.grid = copy.deepcopy(self.previous_grid)

    def step_forward(self):
        """
        Advances the game's state by one time step, updating all cell states
        in the process.
        """

        # Store a copy of the current grid for future reference
        self.previous_grid = copy.deepcopy(self.grid)

        # Update the grid state
        self.update_grid()

    def update_grid(self):
        """
        Update the entire grid for the next generation according to the rules
        of the game variant.

        The update of cell states is done in two steps to avoid interference
        between the new state of a cell and the count of live neighbors for
        its subsequent cells.

        For the "original" variant:
            - The method first counts the live neighbors for each cell.
            - Then it updates the state of each cell based on the original
              rules of the Game of Life.

        For other variants:
            - The method first gets the states of neighboring cells for each
              cell and calculates the new state.
            - Then it updates the state of each cell in the grid with these
              new states.
        """

        # Store a copy of the current grid for future reference
        self.previous_grid = copy.deepcopy(self.grid)

        # Initialize the updated_states list to store new states of each cell
        updated_states = [[] for _ in range(self.grid_size)]

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                # Get neighboring cells' states
                neighboring_states = self.get_neighboring_cells(cell)
                # Calculate the new state of the cell
                updated_states[i].append(cell.update_state(neighboring_states))

        # Update the grid with new states of cells
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.state = updated_states[i][j]

        # Increase time step by one
        self.time_step += 1

    def visualize_grid(self):
        """
        Visualize the grid for observing the game state.
        For the original Game of Life, live cells are represented by 1 and
        dead cells by 0.
        For Problife, cells are represented by a real number in [0, 1].
        """

        if self.variant == "original":
            print('\n'.join(' '.join(str(int(cell.state)) for cell in row)
                            for row in self.grid))
        else:
            print('\n'.join(' '.join(str(cell.state) for cell in row)
                            for row in self.grid))
        print("\n")
