'''
Main Module | G-Rex: Graphicast Recommender

This module guides the user through the process of selecting parameters for a Graphicast recommendation based on initial conditions and questions.
'''

# Modules
from modules.database import load_data_from_json
from modules.start_window import start_gui
from modules.logger import debug
from modules.file_paths import MODEL_DATA_PATH

# Metadata
__author__ = 'Hunter Reeves'
__license__ = 'GPL3'
__maintainer__ = 'Hunter Reeves, NWS Fort Worth'
__email__ = 'hunter.reeves@noaa.gov'
__status__ = 'In Production'
__lastmodified__ = '2023-11-05'

def GUI(data):
    """
    Handles the user interface and determines the best recommendation based on user entry data and both databases.

    Args:
        data (dict): A dictionary containing all of the information in the JSON file.
    """

    # Start G-Rex!
    try:
        start_gui(data)
    except Exception as error:
        debug(f"G-Rex could not be launched! Code: {error}", "ERROR")
        return

def main():
    """
    Starting point for G-Rex!
    """

    # Read in all the data associated with the initial conditions and the decision trees
    try:
        data = load_data_from_json(MODEL_DATA_PATH)
    except Exception as error:
        debug(f"Model data could not be loaded. Code: {error}", "ERROR")
        return
    
    # Launch the recommendation system with all necessary data
    GUI(data)