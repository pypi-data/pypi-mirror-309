import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd

FIG_SIZE_X = 6
FIG_SIZE_Y = 6

def pitch_locations(df: pd.DataFrame | pd.Series, label_column='pitch_type'):
    """
    Plots a 2D scatter plot of pitch coordinates (px, pz) with different colors for each label.
    Includes a strike zone box, with equal axis scaling and y-axis minimum set to the floor of the data.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'px', 'pz', and label_column columns.
        label_column (str): Column to use for labeling points (default is 'pitch_type').
    """
    if not {'px', 'pz'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'px' and 'pz' columns")
    
    if label_column not in df.columns:
        raise ValueError(f"DataFrame must contain the specified label column '{label_column}'")
    
    fig, ax = plt.subplots(figsize=(FIG_SIZE_X, FIG_SIZE_Y))
    
    # Create a scatter plot for each unique label
    unique_labels = df[label_column].unique()
    for label in unique_labels:
        subset = df[df[label_column] == label]
        ax.scatter(subset['px'], subset['pz'], label=label, alpha=0.7)
    
    # Define the strike zone (centered at px = 0, z range = [20/12, 43/12])
    strike_zone = Rectangle(
        (-0.83, 20/12),  # Bottom-left corner of the rectangle
        1.66,            # Width of the strike zone (±0.83 px from center)
        (43 - 20) / 12,  # Height of the strike zone
        edgecolor='red', facecolor='none', linewidth=2, linestyle='--'
    )
    ax.add_patch(strike_zone)  # Add the rectangle to the plot
    
    # Add labels, legend, and title
    ax.set_xlabel('Horizontal Coordinate (px)')
    ax.set_ylabel('Vertical Coordinate (pz)')
    ax.set_title(f'Pitch Locations by {label_column.capitalize()}')
    ax.legend(title=label_column.capitalize())
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Ensure equal scaling for both axes
    ax.set_aspect('equal', adjustable='datalim')
    plt.show()

def pitch_movements(df: pd.DataFrame | pd.Series, label_column='pitch_type'):
    """
    Plots a 2D scatter plot of pitch breaks (breakx and inducedbreakz) with different colors for each label.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'breakx', 'inducedbreakz', and label_column columns.
        label_column (str): Column to use for labeling points (default is 'pitch_type').
    """
    if not {'breakx', 'inducedbreakz'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'breakx' and 'inducedbreakz' columns")
    
    if label_column not in df.columns:
        raise ValueError(f"DataFrame must contain the specified label column '{label_column}'")
    
    fig, ax = plt.subplots(figsize=(FIG_SIZE_X, FIG_SIZE_Y))
    
    # Create a scatter plot for each unique label
    unique_labels = df[label_column].unique()
    for label in unique_labels:
        subset = df[df[label_column] == label]
        ax.scatter(subset['breakx'], subset['inducedbreakz'], label=label, alpha=0.7)
    
    # Set axis limits to represent a 24-inch square space
    ax.set_xlim(-36, 36)
    ax.set_ylim(-36, 36)
    
    # Add labels, legend, and title
    ax.set_xlabel('Horizontal Break (breakx) [inches]')
    ax.set_ylabel('Vertical Break (inducedbreakz) [inches]')
    ax.set_title(f'Pitch Breaks by {label_column.capitalize()}')
    ax.legend(title=label_column.capitalize(), loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Ensure equal aspect ratio
    ax.set_aspect('equal')
    
    plt.show()

def spray_chart(df: pd.DataFrame | pd.Series, label_column='events'):
    """
    Plots a spray chart of batted ball locations using `hc_x_ft` and `hc_y_ft` 
    from a pitch DataFrame. Includes curved foul lines extending 300 feet.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'hc_x_ft', 'hc_y_ft', and label_column.
        label_column (str): Column to use for labeling points (default is 'events').
    """
    if not {'hc_x_ft', 'hc_y_ft'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'hc_x_ft' and 'hc_y_ft' columns")
    
    if label_column not in df.columns:
        raise ValueError(f"DataFrame must contain the specified label column '{label_column}'")

    df = df[df['hc_x_ft'].notna() & df['hc_y_ft'].notna()]
    
    fig, ax = plt.subplots(figsize=(FIG_SIZE_X, FIG_SIZE_Y))

    # Plot each batted ball location with labels
    unique_labels = df[label_column].unique()
    for label in unique_labels:
        subset = df[df[label_column] == label]
        ax.scatter(subset['hc_x_ft'], subset['hc_y_ft'], label=label, alpha=0.7)
    
    # Set labels and title
    ax.set_xlabel('Y from Home Plate (feet)')
    ax.set_ylabel('X Distance from Home Plate (feet)')
    ax.set_title(f'Spray Chart by {label_column.capitalize()}')
    ax.legend(title=label_column.capitalize(), loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Set aspect ratio and orientation
    ax.set_aspect('equal')
    ax.set_xlim(-20, 350)
    ax.set_ylim(-20, 350)
    
    plt.show()
