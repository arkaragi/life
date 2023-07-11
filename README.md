# Life: Interactive GUI for Game of Life and its Variants

The classic Conway's Game of Life with a user-friendly GUI and the implementation of different variants.

## Description

This Python project is an interactive, graphical implementation of the classic cellular automaton known
as the "Game of Life" and its probabilistic variant "Problife". It provides a way to explore, visualize,
and experiment with the system.

## Features

    - Intuitive GUI with real-time visualization of the cellular grid and system evolution.

    - User-adjustable parameters including grid size, cell size, and the initial percentage
      of live cells.

    - Implementation of the original version of the Game of Life with deterministic rules.

    - Implementation of the Probabilistic Game of Life (Problife), where cells evolve based
      on birth and survival probabilities.

    - Modular and well-documented codebase for easy understanding, extension, and contribution.

    - Future plans to explore additional variants, such as the asynchronous updates, long range
      interactions and the Quantum Game of Life.

## Installation and Setup

### 1. Clone the Life repository:

Clone the repository and navigate into the project directory:

    git clone https://github.com/arkaragi/life

    cd life/

### 2. Set up a Python virtual environment:

It's a good practice to create a virtual environment for your Python project. 
This way, you can manage the dependencies of this project separately, without
interfering with your other Python projects or system-wide libraries. 
The following commands will create a new virtual environment in a directory
named "venv".

    python3 -m venv venv

To activate the virtual environment use:

    .\venv\Scripts\activate     (Windows)

    source venv/bin/activate    (Unix/MacOS)

### 3. Install the required dependencies:

Install the required packages with pip:

    pip install -r requirements.txt

### 4. Run the application:
    
    python app.py

### 5. Explore the Game of Life

The GUI will load, and you can set up the grid parameters and rules as per your requirement.
You can choose between the Game of Life or Problife, adjust the grid size, the percentage of
initially alive cells, and define custom rules for cell survival and birth. To start the
simulation, click on the 'Play' button. You can also step through the generations manually 
using the 'Next' button, pause the simulation with the 'Stop' button, or reset the grid to
its initial state with the 'Reset' button.

## Contributing

Contributions to Life are welcome! If you have ideas for new features, improvements,
or bug fixes, please open an issue or submit a pull request. Please ensure to follow
the existing code style.

## License

This project is licensed under the MIT License.
