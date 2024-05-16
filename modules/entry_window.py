'''
Entry Window Module

This module provides the entry window for gathering user information in GRex.
'''

# Imports
import tkinter as tk

# Modules
from modules.user_entry import get_hazard, get_selected_days, get_peak_day, get_peak_day_as_int, get_confidence, get_uncertainty
from modules.database import find_match
from modules.fonts import OPTION_FONT
from modules.file_paths import ICON_PATH

def open_entry_window(root, data, button, splash_label, element_color):
    """
    Disable the initial conditions button and open the entry window.

    Args:
        root (tk.Tk): Root GUI window.
        data (dict): A dictionary containing all of the information in the JSON file.
        button (tk.Button): Button associated with opening the entry window.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").
    """

    # Disble the "enter initial conditions" button when the entry window is opened
    button.config(state = tk.DISABLED)
    entry_gui(root, data, button, splash_label, element_color)

def create_entry_window(root, element_color):
    """
    Create the entry window to take in user input for initial conditions.

    Args:
        root (tk.Tk): Root GUI window.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:   
        entry_window (tk.TopLevel): The entry window GUI.
    """

    # Build the entry window
    entry_window = tk.Toplevel(root)
    entry_window.title("GRex: Entry Window")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_x_scaler = 0.5 # Percentage of the screen to scale up or down, horizontal
    screen_y_scaler = 0.5 # Percentage of the screen to scale up or down, vertical
    screen_placement = 2 # Divides user screen by a value, 2 will place the window in the center

    # Calculate window size based on screen dimensions
    window_width = int(screen_width * screen_x_scaler)  
    window_height = int(screen_height * screen_y_scaler)  

    # Position the window in the center
    x_position = (screen_width - window_width) // screen_placement
    y_position = (screen_height - window_height) // screen_placement

    # Build the window geometry
    entry_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    entry_window.resizable(False, False)
    entry_window.iconbitmap(ICON_PATH)

    # Set entry window color with background of color generated in the start window
    entry_window.configure(bg = element_color)

    # Disable the close button at the top right of the window to force use of cancel button
    entry_window.protocol("WM_DELETE_WINDOW", lambda: None) 

    return entry_window

def add_button_frame(entry_window, element_color):
    """
    Add the submit and cancel buttons at the end of the entry window GUI.

    Args:
        entry_window (tk.TopLevel): The entry window GUI.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").

    Returns:
        button_frame (Frame): Frame for adding buttons to for organization in the GUI window.
    """

    # Create a frame for buttons to center them
    button_frame = tk.Frame(entry_window)
    button_frame.configure(bg = element_color)
    button_frame.pack(pady = 30)

    return button_frame

def submit_button(button_frame, entry_window, hazard, selected_days, peak_day, confidence, uncertainty, data, button, splash_label):
    """
    Add the submit button to the entry window GUI.

    Args:
        button_frame (Frame): Frame for adding buttons to for organization in the GUI window.
        entry_window (tk.TopLevel): The entry window GUI.
        hazard (string): String to store hazard type.
        selected_days (list): List to store selected day indices.
        peak_day (IntVar): Value to hold peak day option.
        confidence(IntVar): Value to hold the confidence option.
        uncertainty (StringVar): Value to hold the uncertainty option. 
        data (dict): A dictionary containing all of the information in the JSON file.
        button (tk.Button): Button associated with opening the entry window.
        splash_label (label): Label holding the splash image.
    """

    # Add the submit button with functionality
    submit_button = tk.Button(button_frame, text = "Submit", font = OPTION_FONT, command = lambda: submit_entry(entry_window, hazard, selected_days, peak_day, confidence, uncertainty, data, button, splash_label))
    submit_button.pack(side = tk.LEFT, padx = 15)

def submit_entry(entry_window, hazard, selected_days, peak_day, confidence, uncertainty, data, button, splash_label):
    """
    Process and store user input, then close the entry window.

    Args:
        entry_window (tk.Toplevel): Entry window GUI.
        hazard (tk.StringVar): Variable containing selected hazard value.
        selected_days (list): List of selected days.
        peak_day (IntVar): Value to hold peak day option.
        confidence(IntVar): Value to hold the confidence option.
        uncertainty (StringVar): Value to hold the uncertainty option. 
        data (dict): A dictionary containing all of the information in the JSON file.
        button (tk.Button): Button associated with opening the entry window.
    """

    # Build the entry dictionary
    entry = build_entry_dict(hazard, selected_days, peak_day, confidence, uncertainty)

    # Process the entry
    process_entry(entry, data, button, entry_window, splash_label)

def build_entry_dict(hazard, selected_days, peak_day, confidence, uncertainty):
    """
    Build and return the entry dictionary.

    Args:
        hazard (tk.StringVar): Variable containing selected hazard value.
        selected_days (list): List of selected days.
        peak_day (IntVar): Value to hold peak day option.
        confidence (IntVar): Value to hold the confidence option.
        uncertainty (StringVar): Value to hold the uncertainty option. 

    Returns:
        dict: The entry dictionary.
    """
    entry = {}
    entry['hazard'] = hazard.get().lower()
    entry['selected_days'] = selected_days
    entry['peak_day'] = get_peak_day_as_int(peak_day, selected_days)
    entry['confidence'] = confidence.get()
    entry['uncertainty'] = uncertainty.get().lower()

    return entry

def process_entry(entry, data, button, entry_window, splash_label):
    """
    Process and store user input, then close the entry window.

    Args:
        entry (dict): Dictionary containing user input.
        data (dict): A dictionary containing all of the information in the JSON file.
        button (tk.Button): Button associated with opening the entry window.
        entry_window (tk.Toplevel): Entry window GUI.
        splash_label: Label associated with splash image.
    """
    # Find a match in the initial conditions database
    find_match(entry, data)

    # Exit the entry window...
    entry_window.destroy()     
    close_entry_window(button)

    # Remove the "Enter Initial Conditions" button
    button.destroy()
    splash_label.destroy()

def cancel_button(button_frame, entry_window, button):
    """
    Add the cancel button to the entry window GUI.

    Args:
        button_frame (Frame): Frame for adding buttons to for organization in the GUI window.
        entry_window (tk.TopLevel): The entry window GUI.
        button (tk.Button): Button associated with opening the entry window.
    """

    # Add the cancel button with functionality
    cancel_button = tk.Button(button_frame, text = "Cancel", font = OPTION_FONT, command = lambda: cancel_entry(entry_window, button))
    cancel_button.pack(side = tk.RIGHT, padx = 15)

def cancel_entry(entry_window, button):
    """
    Close the entry window and re-enable the initial conditions button.

    Args:
        entry_window (tk.Toplevel): Entry window GUI.
        button (tk.Button): Button associated with opening the entry window.
    """

    # Close the entry window and reenable the "enter initial conditions" button on click
    entry_window.destroy()
    button.config(state = tk.NORMAL)

def close_entry_window(button):
    """
    Re-enable the initial conditions button when the entry window is closed.

    Args:
        button (tk.Button): Button associated with opening the entry window.
    """

    # Reenable the button to enter initial conditions
    button.config(state = tk.NORMAL)

def entry_gui(root, data, button, splash_label, element_color):
    """
    Create and display the entry window for user input.

    Args:
        root (tk.Tk): Root GUI window.
        data (dict): A dictionary containing all of the information in the JSON file.
        button (tk.Button): Button associated with opening the entry window.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").
    """
        
    def update_peak_day_menu(*_):
        # Get the count of selected days to update the peak day menu
        selected_count = sum(var.get() for var in var_selected_days)

        # If there is more than one selected day, enable the peak day menu
        if selected_count > 1:
            peak_day_menu.config(state = tk.NORMAL)
            peak_day_menu.configure(font = OPTION_FONT)
            peak_day_menu['menu'].delete(0, 'end') 
            
            # Add selected days to the peak day menu
            selected_day_options = [days[idx] for idx, var in enumerate(var_selected_days) if var.get() == 1]
            
            # Add the labels for each selected day
            for day in selected_day_options:
                peak_day_menu['menu'].add_command(label = day, font = OPTION_FONT, command = lambda value = day: peak_day.set(value))
        else:
            # Disable the peak day menu and reset the default value if selected days goes to one or less
            peak_day_menu.config(state = tk.DISABLED)
            peak_day_menu.configure(font = OPTION_FONT)
            peak_day.set("Peak Day") 
    
    # Days to select from through the program
    days = ["Day 0", "Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    
    # Obtain user entry information from the entry window
    entry_window = create_entry_window(root, element_color)
    hazard = get_hazard(entry_window, element_color)
    var_selected_days, selected_days = get_selected_days(entry_window, days, element_color) 
    peak_day, peak_day_menu = get_peak_day(entry_window, days, element_color)
    confidence = get_confidence(entry_window, element_color)
    uncertainty = get_uncertainty(entry_window, element_color)
    button_frame = add_button_frame(entry_window, element_color)

    # Add the trace to update the peak day menu to add selected days to menu
    for var in var_selected_days:
        var.trace("w", lambda *_: update_peak_day_menu())

    # Add buttons to finialize entry submission at the end, or to exit the entry window completely
    submit_button(button_frame, entry_window, hazard, selected_days, peak_day, confidence, uncertainty, data, button, splash_label)
    cancel_button(button_frame, entry_window, button)