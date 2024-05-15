'''
Database Module

This module provides functions related to handling and processing data for the decision tree model.
'''

# Modules
from modules.logger import log_entry, debug

def load_data_from_json(filename):
    """
    Read the JSON file that has all initial condition and decision tree data inside.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        data (dict): A dictionary containing all of the information in the JSON file.
    """

    # Imports
    import json

    # Open the JSON file
    with open(filename, 'r') as file:
        # Store the data
        data = json.load(file)

    return data

def find_match(entry, data):
    """
    Helper function: Checks if the user entry matches any of the initial conditions.

    Args:
        entry (dict): User input data as a dictionary.
        data (dict): A dictionary containing all of the information in the JSON file.

    Returns:
        str or None: The matching condition if found, otherwise None.
    """
    
    # Check the user entry against initial conditions to find a match, or if there isn't at match at all
    matching_condition = check_entry(entry, data)
    if matching_condition is not None:
        print(f"A match was found! Match: {matching_condition}")
        timestamp = debug("Successful run! Your initial conditions have a match in the decision tree database.", severity = "INFO")
        log_entry(entry, True, timestamp)
    else:
        print("A probabilistic graphicast is not recommended for this forecast scenario.")
        timestamp = debug("A match was not found. Do these initial conditions need to be considered?", severity = "WARNING")
        log_entry(entry, False, timestamp)

def check_entry(entry, data):
    """
    Helper function: Checks if the user entry matches any of the initial conditions.

    Args:
        entry (dict): User input data as a dictionary.
        data (dict): A dictionary containing all of the information in the JSON file.

    Returns:
        dict or None: The matching condition if found, otherwise None.
    """

    # Extract the list of trees from the data
    trees = data.get("trees", [])

    # Iterate through each tree
    for tree in trees:
        # Get the initial conditions from each tree to check for matches
        initial_conditions = tree.get("initial_conditions", {})
        
        if (
            initial_conditions['hazard'] == entry['hazard'] and
            int(initial_conditions['day_min']) <= entry['peak_day'] <= int(initial_conditions['day_max']) and
            int(initial_conditions['conf_min']) <= entry['confidence'] <= int(initial_conditions['conf_max']) and
            initial_conditions['uncertainty'] == entry['uncertainty']
        ):
            return initial_conditions

    return None