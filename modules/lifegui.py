"""
This module defines the LifeGUI class, which provides a Graphical User Interface
(GUI) for running simulations of the Game of Life and its variant, Problife.

The GUI provides a number of parameters for controlling the simulation, including
the size of the grid, the initial seed for the random number generator, the rules
for cells' life and death, the percentage of the initially alive cells and the
speed of the simulation. Users can choose between the Game of Life and Problife
variants, and can start, stop, and step through the simulation as desired.

In addition, users have the ability to edit the grid and change the state of the
cells, while the simulation is running. This interactive feature allows for real
time modifications to individual cells, granting greater flexibility and control
during the simulation.
"""

import copy
import re
import tkinter as tk

from tkinter import messagebox

from life.modules.game import GameOfLife
from life.modules.rule import Rule


class LifeGUI:
    """
    A GUI for controlling simulations of the Game of Life and its variants.

    This class represents a GUI for running and controlling a simulation of
    the Game of Life. It provides various controls for the user to manipulate
    the simulation, including parameters like grid size, initial seed, rules
    for cell life and death, and speed of the simulation. The user can also
    choose between two variants: "Game of Life" and "Problife".

    Parameters
    ----------
    root: tk.Tk
        The root window for the tkinter GUI.

    Attributes
    ----------
    header_font:
        The font for headers in the GUI.

    label_font:
        The font for labels in the GUI.

    animation_running:
        A flag indicating if the simulation is currently running.

    draw_mode:
        A flag indicating if cells are being drawn or erased.

    time_step:
        The number of time steps that have been taken in the current
        simulation.
    """

    # CONSTANTS
    # Min-Max speed slider values
    SPEED_SLIDER_MIN = 1
    SPEED_SLIDER_MAX = 2000
    # Simulation buttons icons
    PLAY_ICON_PATH = 'icons/play_icon.png'
    STOP_ICON_PATH = 'icons/stop_icon.png'
    PREV_ICON_PATH = 'icons/prev_icon.png'
    NEXT_ICON_PATH = 'icons/next_icon.png'
    # Labels
    GAME_OF_LIFE = "Game of Life"
    PROBLIFE = "Problife"
    GRID_SIZE = "Grid Size"
    CELL_SIZE = "Cell Size"
    ALIVE_PERCENTAGE = "Alive Percentage"
    SEED = "Seed"

    def __init__(self, root):
        # Create the main window
        self.root = root

        # Initialize the attributes of the GUI
        self.root.title(LifeGUI.GAME_OF_LIFE)
        self.root.resizable(False, False)
        self.header_font = "Arial 15"
        self.label_font = "Arial 11"
        self.animation_running = False
        self.draw_mode = True
        self.time_step = 0

        # Create a frame for the left panel
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Initialize the necessary tk.Variable objects
        self.__init_tk_variables()

        # Create the Variants frame
        self.create_variants_frame(left_frame)

        # Create the Grid Parameters frame
        self.create_grid_parameters_frame(left_frame)

        #  Create the Rules frame
        self.create_rules_frame(left_frame)

        #  Create the Simulation Parameters frame
        self.create_sim_parameters_frame(left_frame)

        # Create a Status Bar Label at the bottom of the panel
        self.create_status_label(left_frame)

        # Keep the window alive
        self.root.mainloop()

    def __init_tk_variables(self):
        """
        This method is used to initialize tkinter variable objects,
        which are used to store and retrieve values that are manipulated
        in the GUI elements (like Entry, Scale etc.).
        """

        # Set initial value of variant to 'game_of_life'
        self.variants_var = tk.StringVar(value="original")

        # Set initial values for grid parameters
        self.grid_size_var = tk.StringVar(value="20")
        self.cell_size_var = tk.StringVar(value="50")
        self.alive_percentage_var = tk.StringVar(value="0.2")
        self.seed_var = tk.StringVar(value="0")
        self.random_seed_var = tk.BooleanVar(value=True)

        # Set initial values for rules parameters
        self.rule_type_var = tk.StringVar(value="original")
        self.rule1_var = tk.StringVar(value="Ps(2)=1")
        self.rule2_var = tk.StringVar(value="Ps(3)=1")
        self.rule3_var = tk.StringVar(value="Pb(3)=1")
        self.rule4_var = tk.StringVar()
        self.rule5_var = tk.StringVar()
        self.rule6_var = tk.StringVar()
        self.rule7_var = tk.StringVar()
        self.rule8_var = tk.StringVar()

        # Make a container for every rule variable
        self.rule_variables = [
            self.rule1_var,
            self.rule2_var,
            self.rule3_var,
            self.rule4_var,
            self.rule5_var,
            self.rule6_var,
            self.rule7_var,
            self.rule8_var,
        ]

        # Set initial value for the speed of the simulation
        self.speed_entry_var = tk.IntVar(value=1)

    # BELOW WE DEFINE METHODS FOR VALIDATING USER INPUT

    def validate_grid_prmts_entries(self):
        """
        Validate the user inputs for the grid and simulation parameters.

        This method checks if the grid size, cell size, alive percentage,
        and seed are valid. If they are not, it shows an error message to
        the user and returns False. If all inputs are valid, it returns
        True.

        Returns:
        bool:
            True if all inputs are valid, False otherwise.
        """

        if not self.validate_grid_size():
            return False

        if not self.validate_cell_size():
            return False

        if not self.validate_alive_percentage():
            return False

        return True

    def validate_grid_size(self):
        """
        Validates the grid size entered by the user.
        """

        try:
            grid_size = int(self.grid_size_var.get())
            if grid_size <= 1:
                messagebox.showerror("Invalid Input",
                                     "Grid size must be a positive integer (grid_size > 1).")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid number for grid size.", )
            return False

        return True

    def validate_cell_size(self):
        """
        Validates the cell size entered by the user.
        """

        try:
            cell_size = int(self.cell_size_var.get())
            if cell_size <= 0:
                messagebox.showerror("Invalid Input",
                                     "Cell size must be a positive integer (cell_size > 0).")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid number for cell size.", )
            return False

        return True

    def validate_alive_percentage(self):
        """
        Validates the percentage of alive cells entered by the user.
        """

        try:
            alive_percentage = float(self.alive_percentage_var.get())
            if not (0 <= alive_percentage <= 1):
                messagebox.showerror("Invalid Input",
                                     "Alive percentage must be a real number in the range [0, 1].")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid number for the percentage of alive cells.", )
            return False

        return True

    def validate_seed(self):
        """
        Validates the percentage of alive cells entered by the user.
        """

        try:
            seed = int(self.seed_var.get())
            if not (seed >= 0):
                messagebox.showerror("Invalid Input",
                                     "Seed must be a non negative integer (seed >= 0) or None.")
                return False
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid number for the seed parameter.")
            return False

        return True

    def validate_rule(self, expr):
        """
        Validates a custom rule entered by the user.
        """

        # Use a regular expression to validate the rule
        rule_regex = r"^[Pp][SsBb]\(\d\)=\d(\.\d+)?$"

        # If the rule matches the regular expression, it's valid
        if re.fullmatch(rule_regex, expr):
            condition = expr[1].lower()
            neighbor_count = int(expr[3])
            probability = float(expr[6:])

            if 0 <= neighbor_count <= 8 and 0 <= probability <= 1 and condition in ["s", "b"]:
                return True
            else:
                msg = "The assigned number of neighbors must be in range [0, 8] and " \
                      "the assigned probability must be a float in range [0, 1]."
        else:
            msg = ("A valid rule must be of the following form: 'Pc(N)=x',\n"
                   "where 'c' is the condition ('s' for survival, 'b' for birth),\n"
                   "'N' is the number of neighbors (integer from 0 to 8),\n"
                   "and 'x' is the probability (float between 0 and 1).")

        # If we got to this point, the rule is invalid
        messagebox.showerror("Invalid Input", msg)
        return False

    # BELOW WE DEFINE METHODS FOR CREATING THE FRAMES OF THE GUI

    def create_variants_frame(self, parent):
        """
        Create a frame for the Variants setting in the given parent frame.

        Parameters
        ----------
        parent: tk.Frame
            The parent frame in which to create the Variants frame.
        """
        # Create the Variants frame
        self.variants_frame = self.create_label_frame(parent, text="Variants")

        # Create and add a checkbutton for Game of Life
        self.create_checkbutton(self.variants_frame,
                                LifeGUI.GAME_OF_LIFE,
                                self.variants_var,
                                "original")

        # Create and add a checkbutton for Problife
        self.create_checkbutton(self.variants_frame,
                                LifeGUI.PROBLIFE,
                                self.variants_var,
                                "problife")

    def create_grid_parameters_frame(self, parent):
        """
        Create a frame for the Grid Parameters in the given parent frame.

        Parameters
        ----------
        parent: tk.Frame
            The parent frame in which to create the Grid Parameters frame.
        """

        # Create Grid Parameters frame
        self.grid_parameters_frame = self.create_label_frame(parent, text="Grid Parameters")

        # Labels and Entries list
        labels = [
            'Grid Size',
            'Cell Size',
            'Alive Percentage',
            'Seed'
        ]

        entries = [
            self.grid_size_var,
            self.cell_size_var,
            self.alive_percentage_var,
            self.seed_var
        ]

        # Initialize a container for the grid parameter entry boxes
        self.grid_parameters_entries = {}

        # Create and add labels and corresponding entries
        for i, (label_text, entry_var) in enumerate(zip(labels, entries)):

            if label_text == "Seed":
                button = tk.Checkbutton(self.grid_parameters_frame)
                button.config(font=self.label_font,
                              text="Random Seed",
                              variable=self.random_seed_var,
                              command=self.toggle_entry,
                              onvalue=True)
                button.grid(row=i, column=0, padx=5, pady=5)
                i += 1

            label = tk.Label(self.grid_parameters_frame,
                             font=self.label_font,
                             text=label_text)
            label.grid(row=i, column=0, sticky='w', padx=5, pady=5)

            entry = tk.Entry(self.grid_parameters_frame)
            entry.config(font=self.label_font,
                         textvariable=entry_var,
                         width=10,
                         justify="center")
            entry.grid(row=i, column=1, padx=5, pady=5)

            if label_text == "Seed":
                entry.config(state=tk.DISABLED)

            self.grid_parameters_entries[label_text] = entry

        # Create and add Initialize button
        self.initialize_button = tk.Button(self.grid_parameters_frame,
                                           font=self.label_font,
                                           text="Initialize",
                                           justify="center",
                                           command=self.initialize_grid,
                                           bg='lightgreen',
                                           width=10)
        self.initialize_button.grid(row=len(labels) + 1, column=0, padx=5, pady=5, )

        # Create and add Cleanup button
        self.cleanup_button = tk.Button(self.grid_parameters_frame,
                                        font=self.label_font,
                                        text="Clean",
                                        justify="center",
                                        command=self.clean_grid,
                                        state=tk.DISABLED,
                                        width=10)
        self.cleanup_button.grid(row=len(labels) + 1, column=1, padx=5, pady=5)

        # Create and add Reset button
        self.reset_button = tk.Button(self.grid_parameters_frame,
                                      font=self.label_font,
                                      text="Reset",
                                      justify="center",
                                      command=self.reset_grid,
                                      state=tk.DISABLED,
                                      width=10)
        self.reset_button.grid(row=len(labels) + 2, column=0, padx=5, pady=5)

        # Create and add Defaults button
        self.defaults_button = tk.Button(self.grid_parameters_frame,
                                         font=self.label_font,
                                         text="Defaults",
                                         justify="center",
                                         command=self.reset_default_values,
                                         width=10, )
        self.defaults_button.grid(row=len(labels) + 2, column=1, padx=5, pady=5)

    def create_rules_frame(self, parent):
        """
        Create a frame for the Rules in the given parent frame.

        Parameters
        ----------
        parent: tk.Frame
            The parent frame in which to create the Rules frame.
        """

        # Create Rules frame
        self.rules_frame = self.create_label_frame(parent, text="Rules")

        # Create and add a checkbutton for Game of Life
        self.original_rules_button = tk.Checkbutton(self.rules_frame)
        self.original_rules_button.config(font=self.label_font,
                                          text="Original",
                                          variable=self.rule_type_var,
                                          command=self.set_default_rules,
                                          onvalue="original")
        self.original_rules_button.grid(row=0, column=0,
                                        sticky='w', padx=5, pady=5)

        # Create and add a checkbutton for Problife
        self.problife_rules_button = tk.Checkbutton(self.rules_frame)
        self.problife_rules_button.config(font=self.label_font,
                                          text="Problife",
                                          variable=self.rule_type_var,
                                          command=self.set_default_rules,
                                          onvalue="problife")
        self.problife_rules_button.grid(row=0, column=1,
                                        sticky='w', padx=5, pady=5)

        # Create and add a checkbutton for Custom Rules
        self.custom_rules_button = tk.Checkbutton(self.rules_frame)
        self.custom_rules_button.config(font=self.label_font,
                                        text="Custom",
                                        variable=self.rule_type_var,
                                        command=self.set_default_rules,
                                        onvalue="custom")
        self.custom_rules_button.grid(row=0, column=2,
                                      sticky='w', padx=5, pady=5)

        # Create and add rule entries
        rule_labels = [f"Rule {j + 1}" for j in range(8)]
        for i, (rule_text, rule_var) in enumerate(zip(rule_labels, self.rule_variables), start=2):
            label = tk.Label(self.rules_frame,
                             font=self.label_font,
                             text=f"{rule_text}")
            label.grid(row=i, column=0, sticky='w', padx=5, pady=5)

            entry = tk.Entry(self.rules_frame)
            entry.config(font=self.label_font,
                         textvariable=rule_var,
                         width=10,
                         justify="center")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')

        # Create and add Reset button
        self.set_rules_button = tk.Button(self.rules_frame,
                                          font=self.label_font,
                                          text="Set Rules",
                                          command=self.set_rules,
                                          state=tk.DISABLED)
        self.set_rules_button.grid(row=len(rule_labels) + 2, column=0,
                                   sticky='w', padx=5, pady=5)

    def create_sim_parameters_frame(self, parent):
        """
        Create a frame for the Simulation Parameters in the given parent frame.

        Parameters
        ----------
        parent: tk.Frame
            The parent frame in which to create the Simulation Parameters frame.
        """

        # Create Simulation Parameters frame
        self.sim_parameters_frame = self.create_label_frame(parent, text="Simulation Parameters")

        # Create and add Animation Speed label and slider
        speed_label = tk.Label(self.sim_parameters_frame,
                               font=self.label_font,
                               text="Simulation Speed:", )
        speed_label.pack(pady=5)

        self.speed_slider = tk.Scale(self.sim_parameters_frame,
                                     from_=self.SPEED_SLIDER_MIN,
                                     to=self.SPEED_SLIDER_MAX,
                                     orient='horizontal',
                                     resolution=100,
                                     sliderlength=30,
                                     width=20,
                                     command=self.update_speed,
                                     background='light gray',
                                     foreground='black',
                                     troughcolor='dark gray',
                                     sliderrelief='raised')
        self.speed_slider.pack(fill="x")

        # Load icons for buttons
        play_icon = tk.PhotoImage(file=LifeGUI.PLAY_ICON_PATH)
        stop_icon = tk.PhotoImage(file=LifeGUI.STOP_ICON_PATH)
        prev_icon = tk.PhotoImage(file=LifeGUI.PREV_ICON_PATH)
        next_icon = tk.PhotoImage(file=LifeGUI.NEXT_ICON_PATH)

        # Create and add Start, Stop, Next, and Previous buttons
        self.start_button = self.create_image_button(self.sim_parameters_frame,
                                                     play_icon,
                                                     self.start_animation,
                                                     tk.DISABLED)
        self.stop_button = self.create_image_button(self.sim_parameters_frame,
                                                    stop_icon,
                                                    self.stop_animation,
                                                    tk.DISABLED)
        self.prev_step_button = self.create_image_button(self.sim_parameters_frame,
                                                         prev_icon,
                                                         self.prev_step,
                                                         tk.DISABLED)
        self.next_step_button = self.create_image_button(self.sim_parameters_frame,
                                                         next_icon,
                                                         self.next_step,
                                                         tk.DISABLED)

    def create_status_label(self,
                            parent):
        """
        Create a Status Bar Label.
        """

        # Status Bar Label
        self.status_label = tk.Label(parent,
                                     text="Step 1. Initialize the Grid",
                                     bd=1,
                                     relief=tk.SUNKEN,
                                     anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill="x", expand=10)

    def create_grid_frame(self):
        """
        Creates a new window with dimensions of 600x400. The window contains a
        canvas object that will represent the grid of the Game of Life simulation.
        """

        grid_size = int(self.grid_size_var.get())
        cell_size = int(self.cell_size_var.get())

        # Create a new window for the grid canvas
        self.grid_frame = tk.Toplevel(self.root)
        self.grid_frame.geometry(f'{grid_size * cell_size}x{grid_size * cell_size}')
        self.grid_frame.title('The Grid')

        # Create a canvas inside the grid frame
        self.canvas = tk.Canvas(self.grid_frame,
                                width=grid_size * cell_size,
                                height=grid_size * cell_size,
                                borderwidth=0,
                                highlightthickness=0,
                                bg='white')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.handle_mouse_click)

    # BELOW WE DEFINE METHODS FOR INITIALIZING THE GRID

    def initialize_grid(self):
        """
        Initialize the grid based on the user's input parameters.
        Perform validation on user inputs before initializing the grid.
        """

        # Validate user inputs
        if not self.validate_grid_prmts_entries():
            return

        # Destroy the existing grid window if there is one
        if hasattr(self, 'grid_frame') and self.grid_frame is not None:
            self.grid_frame.destroy()
            if self.animation_running:
                self.stop_animation()

        # Create a Canvas object to
        self.create_grid_frame()

        # Retrieve user inputs from GUI
        grid_size = int(self.grid_size_var.get())
        cell_size = int(self.cell_size_var.get())
        alive_percentage = float(self.alive_percentage_var.get())

        # Get the seed if the user defined it
        if self.random_seed_var.get():
            seed = None
        else:
            if not self.validate_seed():
                return False
            seed = int(self.seed_var.get())

        # Clear existing game rules
        Rule.clear_rules()

        # Nullify the steps counter
        self.time_step = 0

        # Initialize the game of life with given parameters
        variant = self.variants_var.get()
        self.life = GameOfLife(variant=variant)
        self.life.initialize_grid(grid_size=grid_size,
                                  alive_percentage=alive_percentage,
                                  seed=seed)

        # Configure the canvas size based on the grid and cell sizes
        self.canvas.config(width=grid_size * cell_size,
                           height=grid_size * cell_size)

        # Draw the initial state of the grid on the canvas
        self.draw_grid()

        # Set the button states for the new grid
        self.cleanup_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.set_rules_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.next_step_button.config(state=tk.DISABLED)
        self.prev_step_button.config(state=tk.DISABLED)

        # Update the status label to indicate that the grid has been initialized
        self.update_status("Step 2. Initialize Rules")

    def draw_grid(self):
        """
        Draw the grid on the canvas. This method handles the animation for both
        the original Game of Life and the Problife simulation.

        In the case of the original Game of Life, cells are drawn as either black
        or white squares to represent alive and dead cells, respectively.
        In the Problife simulation, the state of each cell is a real number in the
        range [0, 1], and the color of the cell goes from blue (representing 0) to
        green (representing 0.5) to red (representing 1) as the state of the cell
        increases.
        """

        # Retrieve grid size from GUI inputs and convert it to an integer
        grid_size = int(self.grid_size_var.get())

        # Retrieve cell size from GUI inputs and convert it to an integer
        cell_size = int(self.cell_size_var.get())

        # Clear any existing grid on the canvas
        self.canvas.delete("all")

        # Handle the simulation of Game of Life
        if self.variants_var.get() == "original":
            # Iterate through each cell in the grid
            for i in range(grid_size):
                for j in range(grid_size):
                    # If the cell is alive (state == 1), draw a black rectangle at its location on the canvas
                    if self.life.grid[i, j].state == 1:
                        self.canvas.create_rectangle(j * cell_size,
                                                     i * cell_size,
                                                     (j + 1) * cell_size,
                                                     (i + 1) * cell_size,
                                                     fill="black")

        # Handle the simulation of Problife
        else:
            # Iterate through each cell in the grid
            for i in range(grid_size):
                for j in range(grid_size):
                    # Determine the cell color based on its state (blue at 0, green at 0.5, red at 1)
                    cell_state = self.life.grid[i, j].state
                    if cell_state == 0:
                        r, g, b, = 255, 255, 255
                    elif 0 < cell_state < 0.5:
                        # Interpolate from blue to green
                        r = 0
                        g = int(cell_state * 2 * 255)
                        b = int((1 - 2 * cell_state) * 255)
                    else:
                        # Interpolate from green to red
                        r = int((cell_state - 0.5) * 2 * 255)
                        g = int((1 - 2 * (cell_state - 0.5)) * 255)
                        b = 0

                    cell_color = "#%02x%02x%02x" % (r, g, b)  # Generate RGB color string

                    # Draw the cell with its color on the canvas
                    self.canvas.create_rectangle(j * cell_size,
                                                 i * cell_size,
                                                 (j + 1) * cell_size,
                                                 (i + 1) * cell_size,
                                                 fill=cell_color)

                    # Display the state of the cell
                    if int(self.cell_size_var.get()) >= 40:
                        self.canvas.create_text((j + 0.5) * cell_size,
                                                (i + 0.5) * cell_size,
                                                text="{:.2f}".format(cell_state))

    def clean_grid(self):
        """
        Clean up the grid and stop the simulation if it is currently running.
        """

        # Reset the grid in the GameOfLife object
        self.life.reset_grid()

        # Clear the grid from the canvas
        self.canvas.delete("all")

        # Enable the Reset button to return the grid to its initial state
        self.reset_button.config(state=tk.NORMAL)

        # Disable the Cleanup button as the grid cannot be cleared now
        self.cleanup_button.config(state=tk.DISABLED)

        # Disable the Start button as the simulation is not running
        self.start_button.config(state=tk.DISABLED)
        if self.set_rules_button["state"] == "disabled":
            self.start_button.config(state=tk.NORMAL)

        # Disable the Stop button as the simulation is not running
        self.stop_button.config(state=tk.DISABLED)

        # Disable the Next Step button as the simulation is not running
        self.next_step_button.config(state=tk.DISABLED)

        # Disable the Previous Step button as the simulation is not running
        self.prev_step_button.config(state=tk.DISABLED)

    def reset_grid(self):
        """
        Reset the simulation grid to its initial state.
        """

        # Reset the grid in the GameOfLife object to the initial state
        self.life.grid = copy.deepcopy(self.life.initial_grid)

        # Draw the initial state of the grid on the canvas
        self.draw_grid()

        # Disable the Reset button as the grid is already in its initial state
        self.reset_button.config(state=tk.DISABLED)

        # Enable the Cleanup button as the grid can be cleared now
        self.cleanup_button.config(state=tk.NORMAL)

        # Disable the Start button as the simulation is not running
        self.start_button.config(state=tk.DISABLED)

        # Disable the Stop button as the simulation is not running
        self.stop_button.config(state=tk.DISABLED)

        # Disable the Next Step button as the simulation is not running
        self.next_step_button.config(state=tk.DISABLED)

        # Disable the Previous Step button as the simulation is not running
        self.prev_step_button.config(state=tk.DISABLED)

    def reset_default_values(self):
        """
        Set default values for the grid parameters.
        """

        # Set the default size of the grid
        self.grid_size_var.set("20")

        # Set the default size of each cell in the grid
        self.cell_size_var.set("50")

        # Set the default percentage of cells that will be alive in the grid
        self.alive_percentage_var.set("0.2")

        # Set the default seed for the random number generator
        self.seed_var.set("0")

        # Set the default usage of the seed
        self.random_seed_var.set(True)

        # Disable the Seed entry field as it is not required when the default seed is in use
        self.grid_parameters_entries["Seed"].config(state=tk.DISABLED)

    # BELOW WE DEFINE METHODS FOR SETTING THE RULES OF THE SIMULATION

    def set_default_rules(self):
        """
        Reset the game rules to their default state.
        """

        # Clear existing game rules
        Rule.clear_rules()

        # Retrieve the type of rules from the GUI
        rule_type = self.rule_type_var.get()

        # Clear all the rule fields
        for variable in self.rule_variables:
            variable.set(value="")

        # For original rule type, get the original rules
        if rule_type == "original":
            Rule.get_original_rules()

        # For problife rule type, get the problife rules
        if rule_type == "problife":
            Rule.get_problife_rules()

        # If the rule type is set to custom, set an example ruleset
        if rule_type == "custom":
            Rule.get_custom_rules()

        # Convert the rules into expressions
        rules_to_expr = [rule.rule_to_expr() for rule in Rule.rules.values()]

        # Set the expressions in the GUI
        for j, rule in enumerate(rules_to_expr):
            self.rule_variables[j].set(rule)

    def set_rules(self):
        """
        Set the game rules based on user input.
        """

        # Clear existing game rules
        Rule.clear_rules()

        # For each rule variable, check if it is valid and if so, convert it to a rule
        for variable in self.rule_variables:
            rule_expr = variable.get()
            if rule_expr != "" and self.validate_rule(rule_expr):
                Rule.expr_to_rule(rule_expr)

        # Set the rules in the game of life object
        self.life.set_rules(original_rules=False, rules=Rule.rules)

        # Update the bottom status bar label
        self.update_status("Step 3. Simulate Model's Evolution")

        # Set the state of the buttons based on the new rules
        self.set_rules_button.config(state=tk.DISABLED)
        self.cleanup_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.next_step_button.config(state=tk.NORMAL)
        self.prev_step_button.config(state=tk.DISABLED)

    # BELOW WE DEFINE METHODS FOR ANIMATING THE SIMULATION

    def animate(self):
        """
        Perform the animation of the Game of Life.

        This method is responsible for updating the grid at each time step and
        drawing it on the canvas. It's a recursive method which schedules itself
        to run again after a small delay, creating the animation effect.
        """

        # If the animation is currently running, perform the next step of the animation
        if self.animation_running:
            # Update the grid to the next time step
            self.life.update_grid()

            # Draw the updated grid on the canvas
            self.draw_grid()

            # Update the status label with a message and the current time step
            self.time_step += 1
            self.update_status(f"Animation Started\n"
                               f"Current Generation: {self.time_step}")

            # Schedule the next call to animate.
            # The after method is a way to schedule something to happen after
            # a certain amount of time. Here, we're scheduling `self.animate()`
            # to be called again after 100ms, creating a cycle, until
            # `self.animation_running` is set to `False`.
            self.root.after(int(self.speed_entry_var.get()), self.animate)

    def start_animation(self):
        """
        Start the animation of the Game of Life.
        """

        if not self.animation_running:
            self.animation_running = True
            self.animate()

            for key, entry in self.grid_parameters_entries.items():
                entry.config(state=tk.DISABLED)

            # Enable/disable buttons
            self.cleanup_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)
            self.set_rules_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.next_step_button.config(state=tk.DISABLED)
            self.prev_step_button.config(state=tk.DISABLED)

    def stop_animation(self):
        """
        Pause the animation of the Game of Life.
        """

        self.animation_running = False

        for key, entry in self.grid_parameters_entries.items():
            if key != "Seed":
                entry.config(state=tk.NORMAL)

        # Enable/disable buttons
        self.cleanup_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.next_step_button.config(state=tk.NORMAL)
        self.prev_step_button.config(state=tk.NORMAL)

        #
        self.update_status(f"Animation Paused\n"
                           f"Current Generation: {self.time_step}")

    def next_step(self):
        """Advances the simulation by a single step."""

        # If the simulation isn't running, update the grid once and redraw it
        if not self.animation_running:
            self.life.update_grid()
            self.draw_grid()
            self.time_step += 1
            self.update_status(f"Step Forward\n"
                               f"Current Generation: {self.time_step}")

        self.cleanup_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

        if self.time_step >= 1:
            self.prev_step_button.config(state=tk.NORMAL)

    def prev_step(self):
        """Advances the simulation by a single step."""

        # If the simulation isn't running, update the grid once and redraw it
        if not self.animation_running and self.time_step > 0:
            self.life.step_backwards()
            self.draw_grid()
            self.time_step -= 1
            self.update_status(f"Step Backwards\n"
                               f"Current Generation: {self.time_step}")

            self.prev_step_button.config(state=tk.DISABLED)

        self.cleanup_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)

    def update_speed(self, value):
        """Update the speed of the simulation based on slider value."""

        #
        speed = int(value)
        self.speed_entry_var.set(speed)

    # BELOW WE DEFINE UTILITY METHODS FOR THE GUI

    def create_checkbutton(self, parent, text, variable, onvalue):
        """Helper function to create a checkbutton."""
        button = tk.Checkbutton(parent)
        button.config(font=self.label_font,
                      text=text,
                      variable=variable,
                      onvalue=onvalue)
        button.pack(anchor="w")

    def create_image_button(self, parent, icon, command, state):
        """Helper function to create a button with an image."""
        button = tk.Button(parent, image=icon, command=command, state=state)
        button.image = icon
        button.pack(side="left", padx=5, pady=5)
        return button

    def create_label_frame(self, parent, text):
        """Helper function to create a label frame."""
        frame = tk.LabelFrame(parent, font=self.header_font, text=text)
        frame.pack(fill="x", expand=True, padx=10, pady=10)
        return frame

    def handle_mouse_click(self, event):
        """
        Handle the mouse click event on the canvas.

        Parameters
        ----------
        event: Event
            The mouse click event object.
        """

        cell_size = int(self.cell_size_var.get())
        if self.draw_mode:

            col = event.x // cell_size
            row = event.y // cell_size

            if 0 <= col < self.life.grid_size and 0 <= row < self.life.grid_size:
                # Toggle the state of the cell
                self.life.grid[row, col].state = 1 - self.life.grid[row, col].state

                # Check the type of simulation
                if self.variants_var.get() == "original":
                    color = "black"
                    if self.life.grid[row, col].state == 0:
                        color = "white"
                else:
                    color = "red"
                    if self.life.grid[row, col].state == 0:
                        color = "white"

                # Draw the rectangle
                self.canvas.create_rectangle(col * cell_size,
                                             row * cell_size,
                                             (col + 1) * cell_size,
                                             (row + 1) * cell_size,
                                             fill=color)

                # If the cell size is large enough, draw the state's probability
                if cell_size >= 40 and self.life.grid[row, col].state != 0:
                    self.canvas.create_text((col + 0.5) * cell_size,
                                            (row + 0.5) * cell_size,
                                            text="{:.2f}".format(self.life.grid[row, col].state))

    def toggle_entry(self):
        """

        """

        if self.random_seed_var.get():
            self.grid_parameters_entries["Seed"].config(state=tk.DISABLED)
        else:
            self.grid_parameters_entries["Seed"].config(state=tk.NORMAL)

    def update_status(self, message):
        """
        Update the status bar with the given message.

        Parameters
        ----------
        message: str
            The message to display in the status bar.
        """
        self.status_label.config(text=message)


if __name__ == "__main__":
    toor = tk.Tk()
    LifeGUI(toor)
