'''
Start Window Module

This module provides the starting window for GRex.
'''

# Imports
import tkinter as tk

# Modules
from modules.entry_window import open_entry_window
from modules.fonts import OPTION_FONT
from modules.file_paths import ICON_PATH, SPLASH_IMAGE_PATH

def create_start_window():
    """
    Create and configure the main GUI window.

    Returns:
        root (tk.Tk): The main GUI window.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").
    """

    root = tk.Tk()
    root.title("G-Rex: Main Window")
    
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    screen_x_scaler = 0.3 # Percentage of the screen to scale up or down, horizontal
    screen_y_scaler = 0.5 # Percentage of the screen to scale up or down, vertical
    screen_placement = 2 # Divides user screen by a value, 2 will place the window in the center

    # Calculate window size based on screen dimensions
    window_width = int(screen_width * screen_x_scaler)  
    window_height = int(screen_height * screen_y_scaler)  

    # Position the window in the center
    x_position = (screen_width - window_width) // screen_placement
    y_position = (screen_height - window_height) // screen_placement

    # Build the window geometry
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.resizable(False, False)
    root.iconbitmap(ICON_PATH)

    # Change background color
    element_color = '#DDD0C8' # Medium-light beige
    root.configure(bg = element_color)  

    return root, element_color

def add_spash_image(root):
    """
    Adds the G-Rex mascot to the main GUI window at the start!

    Args:
        root (tk.Tk): The main GUI window.

    Returns:
        splash_label (tk.Label): The label that contains the splash image.
    """

    # Load the image
    image_path = SPLASH_IMAGE_PATH  
    image = tk.PhotoImage(file = image_path)
    pixel_scaler = 2 # Scale the image by every nth pixel - n being the value of pixels skipped
    scaled_image = image.subsample(pixel_scaler)

    # Create a label to display the image
    splash_label = tk.Label(root, image = scaled_image)
    splash_label.image = scaled_image  # Keep a reference to prevent garbage collection
    splash_label.grid(row = 0, pady = 0, sticky = "n")

    return splash_label

def add_entry_button(root, data, splash_label, element_color):
    """
    Add a button to enter initial conditions.

    Args:
        root (tk.Tk): The main GUI window.
        data (dict): A dictionary containing all of the information in the JSON file.
        splash_label (tk.Label): The label that contains the splash image.
        element_color (str): The color in hexadecimal format (e.g., "#RRGGBB").
    """
    
    # Add button to open entry window and submit user entry information for initial conditions
    button = tk.Button(root, text = "Enter Initial Conditions", font = OPTION_FONT, command = lambda: open_entry_window(root, data, button, splash_label, element_color))
    button.grid(row = 1, pady = 0, sticky = "s")  

def configure_grid_weights(root):
    """
    Configure grid row and column weights to center elements both horizontally and vertically.

    Args:
        root (tk.Tk): The main GUI window.
    """

    # Configure the grid for GUI elements in the starting window
    root.grid_rowconfigure(0, weight = 1)
    root.grid_rowconfigure(2, weight = 1)
    root.grid_columnconfigure(0, weight = 1)

def start_gui(data):
    """
    Initialize and start the main GUI window.

    Args:
        data (dict): A dictionary containing all of the information in the JSON file.
    """

    # Build the starting GUI window
    root, element_color = create_start_window()
    splash_label = add_spash_image(root)
    add_entry_button(root, data, splash_label, element_color)
    configure_grid_weights(root)
    root.mainloop()