import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_voltage_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                        y_axis_label="ordinate", type="line"):
    if type == "bar":
        y_pos = np.arange(len(x_vals))
        plt.bar(y_pos, y_vals, align='center', alpha=0)

        y_vals_series = pd.Series.from_array(y_vals)
        ax = y_vals_series.plot(kind='bar')
        add_value_labels(ax)

        plt.xticks(y_pos, x_vals)
        plt.title(title, fontsize=20)
        plt.ylabel(y_axis_label, fontsize=16, labelpad=10)
        plt.yticks(fontsize=16)
        plt.xlabel(x_axis_label, fontsize=16, labelpad=10)
        plt.xticks(fontsize=16)
        plt.ylim(0.8, 1.1)
        plt.show()

    elif type == "line":
        plt.xlabel(x_axis_label, fontsize=16)
        plt.xticks(fontsize=16)
        plt.ylabel(y_axis_label, fontsize=16)
        plt.yticks(fontsize=16)
        plt.title(title, fontsize=20)
        plt.grid(True)
        plt.plot(x_vals, y_vals)
        plt.show()


def create_current_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                        y_axis_label="ordinate"):
    y_pos = np.arange(len(x_vals))
    plt.bar(y_pos, y_vals, align='center', alpha=0)

    y_vals_series = pd.Series.from_array(y_vals)
    ax = y_vals_series.plot(kind='bar')
    add_value_labels(ax)

    plt.xticks(y_pos, x_vals)
    plt.title(title, fontsize=20)
    plt.ylabel(y_axis_label, fontsize=16, labelpad=20)
    plt.yticks(fontsize=16)
    plt.xlabel(x_axis_label, fontsize=16, labelpad=5)
    plt.xticks(fontsize=16)
    plt.show()


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.3f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            va=va)  # Vertically align label differently for
        # positive and negative values.
