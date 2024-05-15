'''
User Entry Module

This module handles the logic for obtaining user input in the entry window.
'''

# Imports
import tkinter as tk

# Modules
from modules.fonts import LABEL_FONT, OPTION_FONT

def get_hazard(entry_window, element_color):
    """
    Creates the section for getting the hazard information from the entry window.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        var_hazard (StringVar): The hazard the user selected.
    """

    # Create a frame to center the hazard label
    hazard_frame = tk.Frame(entry_window)
    hazard_frame.configure(bg = element_color)
    hazard_frame.pack(expand = True, fill = 'both')  # Expand to fill the window

    # Add label for hazard selection
    hazard_label = tk.Label(hazard_frame, text = "What is the main hazard you are messaging?")
    hazard_label.configure(bg = element_color, font = LABEL_FONT)
    hazard_label.pack(pady = (20, 10))

    # Set hazard options
    hazard_types = ["Heavy Rain"] # Adjust hazard options here
    var_hazard = tk.StringVar()
    var_hazard.set(value = hazard_types[0])  # Severe as default value, first type

    # Frame for radial buttons
    radial_frame = tk.Frame(entry_window)
    radial_frame.configure(bg = element_color)
    radial_frame.pack()

    # Go through each option for the radial buttons
    for hazard in hazard_types:
        rad = tk.Radiobutton(radial_frame, text = hazard, variable = var_hazard, value = hazard)
        rad.configure(bg = element_color, activebackground = element_color, font = OPTION_FONT)
        rad.pack(side = 'left', padx = 20)

    return var_hazard

def get_selected_days(entry_window, days, element_color):
    """
    Creates the section for getting the selected days information from the entry window.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        days (list): List of available days for selection.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        var_selected_days (List): List of tkinter IntVar objects representing selected days.
        selected_days (List): List of integer values representing selected days.
    """

    # Checkbox menu for selecting days
    var_selected_days = tk.StringVar()
    selected_days = []

    # Create a frame to center the selected days label
    days_frame = tk.Frame(entry_window)
    days_frame.configure(bg = element_color)
    days_frame.pack(expand = True, fill = 'both')  # Expand to fill the window

    # Add label for hazard selection
    days_label = tk.Label(days_frame, text = "What are the days your hazard is expected to occur?")
    days_label.configure(bg = element_color, font = LABEL_FONT)
    days_label.pack(pady = (20, 0))

    # Frame for the checkbuttons
    checkbutton_frame = tk.Frame(entry_window)
    checkbutton_frame.configure(bg = element_color)
    checkbutton_frame.pack(pady = 20)  # Adjust the padding as needed

    # Update the selected days chosen
    var_selected_days = []
    for _, day in enumerate(days):
        var_day = tk.IntVar()
        cb = tk.Checkbutton(checkbutton_frame, text = day, variable = var_day, onvalue = 1, offvalue = 0, command = lambda: update_selected_days(selected_days, days, var_selected_days))
        cb.configure(bg = element_color, activebackground = element_color, font = OPTION_FONT)
        cb.pack(side = 'left', padx = 10)
        var_selected_days.append(var_day)

    # Get the actual integer value for selected days
    selected_days = [var.get() for var in var_selected_days]

    # Check if all days are unselected
    if all(day == 0 for day in selected_days):
        selected_days = [0]  # Default to selected day of 0 if nothing is selected

    return var_selected_days, selected_days

def update_selected_days(selected_days, days, var_selected_days):
    """
    Helper function: Update the list of selected days based on user input.

    Args:
        selected_days (list): List to store selected day indices.
        days (list): List of day options.
        var_selected_days (list): List of tk.IntVar variables for checkbuttons.
    """

    # Reset selected days to prepare for additional selections
    selected_days.clear()

    # Go through the day options and add the ones that have been selected most recently
    for i, _ in enumerate(days):
        if var_selected_days[i].get() == 1:
            selected_days.append(i)

def get_peak_day(entry_window, days, element_color):
    """
    Creates the section for getting the peak day selection from a drop-down menu containing the selected days chosen previously.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        days (list): List of available days for selection.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        var_peak_day (StringVar): String variable to hold the peak day from the option menu.
        peak_day_menu (OptionMenu): The option menu for selecting the peak day.
    """

    # Frame the peak day section
    peak_day_frame = tk.Frame(entry_window)
    peak_day_frame.configure(bg = element_color)
    peak_day_frame.pack(expand = True, fill = 'both')

    # Add the label for peak day, adjust
    peak_day_label = tk.Label(peak_day_frame, text = "Of your selections, which day is the peak intensity expected to occur?")
    peak_day_label.configure(bg = element_color, font = LABEL_FONT)
    peak_day_label.pack(pady = (10, 0))

    # To store the user-selected peak day
    var_peak_day = tk.StringVar()
    var_peak_day.set("Peak Day")

    # Add the menu with peak day options, start disabled
    peak_day_menu = tk.OptionMenu(peak_day_frame, var_peak_day, *days)
    peak_day_menu.configure(state = 'disabled', font = LABEL_FONT)
    peak_day_menu.pack(pady = (10, 0))

    return var_peak_day, peak_day_menu

def get_peak_day_as_int(var_peak_day, selected_days):
    """
    Get the selected peak day as an integer value.

    Args:
        var_peak_day (StringVar): String variable containing the selected peak day.

    Returns:
        int or None: Integer value of the selected peak day, or None if no day is selected.
    """

    # Check if a peak day value has been selected
    if var_peak_day is not None:
        # Get the peak day to check
        selected_day = var_peak_day.get()

        # If it is not the default value, resturn the selected day
        if selected_day != "Peak Day":
            return int(selected_day.split()[-1])

    # If var_peak_day is None or "Peak Day" is selected, return the first value of selected_days
    if selected_days:
        return selected_days[0]
    
    return None
    
def get_confidence(entry_window, element_color):
    """
    Create a GUI element to obtain the user's confidence level in W/W/A criteria being met.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        tk.IntVar: Variable that holds the selected confidence level.
    """

    def on_radiobutton_select():
        """
        Handle the selection of a radio button.

        This function is called whenever a radio button is selected to update the confidence variable.

        Returns:
            None
        """

        # Get the value for confidence
        _ = var_confidence.get()

    # Frame the section for the confidence selections
    confidence_frame = tk.Frame(entry_window)
    confidence_frame.configure(bg = element_color)
    confidence_frame.pack(expand = True, fill = 'both')

    # Label for confidence section and adjustments
    confidence_label = tk.Label(confidence_frame, text = "What is your forecast confidence in W/W/A criteria being met?")
    confidence_label.configure(bg = element_color, font = LABEL_FONT)
    confidence_label.pack(pady = (0, 25))

    # Initialize the confidence value
    var_confidence = tk.IntVar(value = 10)  # 10% selected by default

    # Frame the radials and adjust
    radial_frame = tk.Frame(confidence_frame)
    radial_frame.configure(bg = element_color)
    radial_frame.pack()

    # Add radial options from 10 to 90 for confidence selections (adjust radial options here)
    for value in range(10, 100, 10):
        # Add the radial buttons from 10 to 90
        rad = tk.Radiobutton(radial_frame, text = str(value), variable = var_confidence, value = value)
        rad.configure(bg = element_color, activebackground = element_color, font = OPTION_FONT)
        rad.pack(side = 'left', padx = 10)

    # Get the value for confidence
    var_confidence.trace("w", lambda *_: on_radiobutton_select())

    return var_confidence

def get_uncertainty(entry_window, element_color):
    """
    Create a GUI element to obtain the user's uncertainty type.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        tk.StringVar: Variable that holds the selected uncertainty type.
    """
        
    # Frame for uncertainty section
    uncertainty_frame = tk.Frame(entry_window)
    uncertainty_frame.configure(bg = element_color)
    uncertainty_frame.pack(expand = True, fill = 'both')

    # Label for uncertainty and adjustments
    uncertainty_label = tk.Label(uncertainty_frame, text = "Is your uncertainty more synoptic (i.e. will all the ingredients align?) or areal (i.e., ingredients should align, but unsure where?)")
    uncertainty_label.configure(bg = element_color, font = LABEL_FONT)
    uncertainty_label.pack(pady = (20, 20))

    # Add types for uncertainty
    uncertainty_types = ["Synoptic", "Areal"] # Add more types here
    var_uncertainty = tk.StringVar(value = uncertainty_types[0])  # Set the initial value to synoptic

    # Add the frame for the radials and adjust
    radial_frame = tk.Frame(uncertainty_frame)
    radial_frame.configure(bg = element_color)
    radial_frame.pack()

    # Add the options for uncertainty
    for uncertainty in uncertainty_types:
        rad = tk.Radiobutton(radial_frame, text = uncertainty, variable = var_uncertainty, value = uncertainty)
        rad.configure(bg = element_color, activebackground = element_color, font = OPTION_FONT)
        rad.pack(side = 'left', padx = 20)

    return var_uncertainty