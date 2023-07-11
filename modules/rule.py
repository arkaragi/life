"""
This module provides an approach for defining and managing custom rules in the
Game of Life and its probabilistic variant, Problife.

The primary class in this module, Rule, encapsulates a single rule and offers
a flexible interface for defining conditions under which a cell survives ('s')
or is born ('b'). Rules are characterized by the number of alive neighboring
cells and an associated probability of transition under those conditions.
"""

import re


class Rule:
    """
    A Rule object represents a single rule in a cellular automaton system,
    characterized by a condition of survival or birth, the number of alive
    neighboring cells, and the associated probability of transition under
    those conditions

    Rules are globally maintained in the class and can be managed through
    various class methods. This structure allows users to define, manipulate
    and apply complex rule sets in a cellular automaton environment.

    Parameters
    ----------
    condition: str
        A string indicating the survival ('s') or birth ('b') condition.

    n_neighbors: int
        An integer representing the count of a cell's alive neighbors for
        which the rule applies.

    probability: float
        The probability that the rule will be applied.
    """

    # Holds the initialized rules
    rules = {}

    # Counts the number of rules inside the rules dictionary
    n_rules = 0

    def __init__(self,
                 condition: str,
                 n_neighbors: int,
                 probability: float):
        # Validate the 'condition' parameter
        if condition not in ['s', 'b']:
            raise ValueError("Condition must be 's' or 'b'")
        # Validate the 'n_neighbors' parameter
        if not isinstance(n_neighbors, int) or n_neighbors < 0:
            raise ValueError("Number of neighbors must be a non-negative integer")
        # Validate the 'probability' parameter
        if not isinstance(probability, (int, float)) or not 0 <= probability <= 1:
            raise ValueError("Probability must be a float between 0 and 1")

        # Check if a similar rule already exists
        for rule in Rule.rules.values():
            if rule.condition == condition and rule.n_neighbors == n_neighbors:
                if rule.probability != probability:
                    print(f"Updated rule P{condition}({n_neighbors}) from {rule.probability} to {probability}")
                    rule.probability = probability
                return

        # Assign the validated parameters to instance variables
        self.condition = condition
        self.n_neighbors = n_neighbors
        self.probability = probability
        # Store the instance in the 'rules' dictionary
        Rule.rules[Rule.n_rules] = self
        # Increment the rule count
        Rule.n_rules += 1

    def rule_to_expr(self):
        """
        Returns a string representation of the Rule object.
        The string format is 'Pc(N)=x', where 'c' is the condition ('s' or 'b'),
        'N' is the number of neighbors, and 'x' is the probability.

        Returns
        -------
        rule_expr: str
            The string representation of the Rule object.
        """

        # Get the string representation of the Rule object.
        rule_expr = f"P{self.condition}({self.n_neighbors})={self.probability}"
        return rule_expr

    @classmethod
    def clear_rules(cls):
        """
        Clear all the defined rules.
        """

        # Reset the rules dictionary
        Rule.rules = {}
        Rule.n_rules = 0

    @classmethod
    def delete_rule(cls, 
                    condition: str, 
                    n_neighbors: int):
        """
        Delete a specific rule if it exists.

        Parameters
        ----------
        condition: str
            The condition of the rule to delete ('s' or 'b').

        n_neighbors: int
            The number of neighbors of the rule to delete.
        """

        # Find the key of the rule to delete
        for key, rule in cls.rules.items():
            if rule.condition == condition and rule.n_neighbors == n_neighbors:
                # Delete the rule
                del cls.rules[key]
                print(f"Rule P{condition}({n_neighbors}) has been deleted.")
                return

        raise ValueError(f"No rule with condition {condition} and {n_neighbors} neighbors found")

    @classmethod
    def display_rules(cls):
        """
        Prints all currently defined rules in a user-friendly way.
        """

        # Print the currently defined rules
        print("Currently defined rules:")
        for rule in cls.rules.values():
            print(f"P{rule.condition}({rule.n_neighbors})={rule.probability}")

    @classmethod
    def expr_to_rule(cls,
                     expr: str):
        """
        Creates a Rule object from a string expression of the form 'Pc(N)=x'.

        Parameters
        ----------
        expr: str
            The string representation of a Rule object. It should follow the format
            'Pc(N)=x', where 'c' is the condition ('s' for survival or 'b' for birth),
            'N' is the number of neighbors, and 'x' is the probability.

        Returns
        -------
        Rule
            The Rule object created from the string expression.

        Raises
        ------
        ValueError
            If the input string does not follow the expected format.
        """

        # Use regex to match the string expression to the expected format 'Pc(N)=x'
        match = re.fullmatch(r"P([sb])\((\d+)\)=(\d+(?:\.\d+)?)", expr)

        if match:
            # Extract the condition, number of neighbors, and probability from the matched groups
            condition, n_neighbors, probability = match.groups()

            # Convert the number of neighbors and probability to int and float, respectively
            n_neighbors = int(n_neighbors)
            probability = float(probability)

            if 0 <= probability <= 1:
                # If the probability is valid (between 0 and 1), create and return a Rule object
                return Rule(condition, n_neighbors, probability)
            else:
                # If the probability is not valid, raise a ValueError
                raise ValueError(f"The assigned probability must be a float in range [0, 1].")
        else:
            # If the string expression does not match the expected format, raise a ValueError
            raise ValueError(f"The expression must start with the letter `P` and be "
                             f"of the form: `Pc(N)=x`, where c, N and X are the condition, "
                             f"the number of neighbors and the probability, respectively.")

    @classmethod
    def get_custom_rules(cls):
        """
        Retrieves an example of custom rules of the Game of Life.

        Returns
        -------
        custom_rules: dict
            A dictionary containing the custom rules for the Game of Life.
        """

        # Define the original rules of the Game of Life
        # Rules 1/2: Any live cell with two or three live neighbors survives
        # Rules 3/4: Any live cell with one or three live neighbors survives
        custom_rules = {
            0: Rule("s", 2, 1),
            1: Rule("s", 3, 1),
            2: Rule("b", 1, 1),
            3: Rule("b", 3, 1),
        }

        return custom_rules

    @classmethod
    def get_original_rules(cls):
        """
        Retrieves the original rules of the Game of Life.

        Returns
        -------
        original_rules: dict
            A dictionary containing the original rules of the Game of Life.
        """

        # Define the original rules of the Game of Life
        # Rule 1: Any live cell with two live neighbors survives
        # Rule 2: Any live cell with three live neighbors survives
        # Rule 3: Any dead cell with three live neighbors becomes a live cell
        original_rules = {
            1: Rule("s", 2, 1),
            2: Rule("s", 3, 1),
            3: Rule("b", 3, 1),
        }

        return original_rules

    @classmethod
    def get_problife_rules(cls):
        """
        Retrieves the rules of Problife.

        Returns
        -------
        problife_rules: dict
            A dictionary containing the original rules of the Problife.
        """

        # Define the original rules of the Game of Life
        problife_rules = {
            1: Rule("s", 2, 0.9),
            2: Rule("s", 3, 0.9),
            3: Rule("b", 3, 0.8),
        }

        return problife_rules

    @classmethod
    def get_rules_by_condition(cls):
        """
        Retrieves the rules categorized by their conditions: survival ('s')
        and birth ('b').

        This method processes the defined rules and groups them based on their
        conditions. It creates a dictionary where the keys are the conditions
        ('s' and 'b') and the values are lists of the number of neighbors for
        which each condition applies.

        Returns
        -------
        rules_by_condition: dict
            A dictionary containing the conditions for survival and birth of cells,
            based on the defined rules. The dictionary's keys are the conditions
            ('s' and 'b'), and the values are lists of the number of neighbors for
            which each condition applies.
        """

        # Initialize an empty dictionary to hold the rules by their condition
        rules_by_condition = {"s": [], "b": []}

        # For each possible condition ('s' and 'b')
        for condition in ["s", "b"]:
            # Iterate over each rule in the class-level 'rules' dictionary
            for rule in cls.rules.values():
                # If the rule's condition matches the current condition being processed
                if rule.condition == condition:
                    # Add the rule's number of neighbors to the appropriate list in the dictionary
                    rules_by_condition[condition].append(rule.n_neighbors)

        return rules_by_condition

    @classmethod
    def get_rules_by_neighbors(cls):
        """
        Retrieves the rules categorized by the number of neighbors.

        This method processes the defined rules and groups them based on the
        number of neighbors for which they apply. It creates a dictionary
        where the keys are the numbers of neighbors, and the values are lists
        of rules applicable to cells with that number of neighbors.

        Returns
        -------
        rules_by_neighbors: dict
            A dictionary containing the conditions for survival and birth of cells,
            based on the defined rules. The dictionary's keys are the numbers of
            neighbors, and the values are lists of rules applicable to cells with
            that number of neighbors.
        """

        # Initialize an empty dictionary to hold the rules by their number of neighbors
        rules_by_neighbors = {}

        # Iterate over each rule in the class-level 'rules' dictionary
        for rule in cls.rules.values():
            # Append the rule to the appropriate key in the dictionary
            rules_by_neighbors.setdefault(rule.n_neighbors, []).append(rule)

        return rules_by_neighbors

    @classmethod
    def update_rule(cls,
                    condition: str,
                    n_neighbors: int,
                    probability: float):
        """
        Update a rule in the rules dictionary if it exists.

        Parameters
        ----------
        condition: str
            The condition of the rule to update ('s' or 'b').

        n_neighbors: int
            The number of neighbors of the rule to update.

        probability: float
            The new probability to assign to the rule.
        """

        # Check if the rule exists
        for rule in Rule.rules.values():
            if rule.condition == condition and rule.n_neighbors == n_neighbors:
                # Update the probability of the rule
                rule.probability = probability
                return
        raise ValueError(f"No rule with condition {condition} and "
                         f"{n_neighbors} neighbors found")
