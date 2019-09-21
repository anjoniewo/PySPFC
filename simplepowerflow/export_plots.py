import math

import matplotlib.pyplot as plt
import numpy as np

from constants import *
from simplepowerflow.csvexport import MAX_NUM_OF_NODES


class Plotter:
    def __init__(self, settings):
        self.__settings = settings

    def export_node_voltage_plots(self, grid_node_timeseries_results, grid_node_min_max_results):
        """
        calls create_voltage_plot() and ... with specified parameters
        """

        settings = self.__settings
        v_nom = 1 if settings.is_export_pu else settings.v_nom
        node_voltages = dict()

        y_label = 'Voltage in pu \u2192' if settings.is_export_pu else 'Voltage in kV \u2192'

        if grid_node_timeseries_results[TIMESTAMP]:
            timestamps = dict(
                [(key, value) for key, value in grid_node_timeseries_results.items() if key == TIMESTAMP])
            del grid_node_timeseries_results[TIMESTAMP]
            node_voltages = grid_node_timeseries_results

            title = 'Time variant Bus voltages'
            x_label = 'Time \u2192'

        self.create_voltage_plot_timeseries(x_vals=timestamps, y_vals=node_voltages, title=title, x_axis_label=x_label,
                                            y_axis_label=y_label)

        if len(timestamps) > 1:
            # die X-Werte:
            grid_nodes = list()
            # die Y-Werte:
            node_voltages = list()
    
            grid_node_min_results = grid_node_min_max_results['max']
            for grid_node_name in grid_node_min_results:
                grid_nodes.append(grid_node_name)
                node_voltages.append(grid_node_min_results[grid_node_name]['v_magnitude'] * v_nom)
    
            title = 'Bus Voltages At Minimal Grid Load'
            x_label = 'Grid Nodes'
    
            self.create_voltage_plot(x_vals=grid_nodes, y_vals=node_voltages, title=title, x_axis_label=x_label,
                                     y_axis_label=y_label)
    
            # die X-Werte:
            grid_nodes = list()
            # die Y-Werte:
            node_voltages = list()
    
            grid_node_max_results = grid_node_min_max_results['min']
            for grid_node_name in grid_node_max_results:
                grid_nodes.append(grid_node_name)
                node_voltages.append(grid_node_max_results[grid_node_name]['v_magnitude'] * v_nom)
    
            title = 'Bus Voltages At Maximal Grid Load'
    
            self.create_voltage_plot(x_vals=grid_nodes, y_vals=node_voltages, title=title, x_axis_label=x_label,
                                     y_axis_label=y_label)

    def export_currents_on_lines_plots(self, grid_line_timeseries_results, grid_line_min_max_results):
        """
        calls create_current_plot() with specified parameters
        """

        settings = self.__settings
        v_nom, s_nom = settings.v_nom, settings.s_nom
        current_nom = s_nom / (v_nom * math.sqrt(3))

        y_label = 'Current in A \u2192'

        if grid_line_timeseries_results[TIMESTAMP]:
            timestamps = dict(
                [(key, value) for key, value in grid_line_timeseries_results.items() if key == TIMESTAMP])
            del grid_line_timeseries_results[TIMESTAMP]
            line_currents = grid_line_timeseries_results

            title = 'Time variant Current on lines'
            x_label = 'Time \u2192'

            self.create_current_plot_timeseries(x_vals=timestamps, y_vals=line_currents, title=title,
                                                x_axis_label=x_label,
                                                y_axis_label=y_label)
            if len(timestamps) > 1:
                # die X-Werte:
                grid_lines = list()
                # die Y-Werte:
                current_on_lines = list()
    
                grid_line_min_results = grid_line_min_max_results['max']
                for grid_line_name in grid_line_min_results:
                    grid_lines.append(grid_line_name)
                    current_on_lines.append(grid_line_min_results[grid_line_name]['current_from_i_to_j'])
    
                current_on_lines = list(map(lambda value: value * current_nom, current_on_lines))
    
                title = 'Current On Lines At Minimal Grid Load'
                x_label = 'Grid Lines'
    
                self.create_current_plot(x_vals=grid_lines, y_vals=current_on_lines, title=title,
                                         x_axis_label=x_label, y_axis_label=y_label)
    
                # die X-Werte:
                grid_lines = list()
                # die Y-Werte:
                current_on_lines = list()
    
                grid_line_max_results = grid_line_min_max_results['min']
                for grid_line_name in grid_line_max_results:
                    grid_lines.append(grid_line_name)
                    current_on_lines.append(grid_line_max_results[grid_line_name]['current_from_i_to_j'])
    
                current_nom = settings.s_nom / (settings.v_nom * math.sqrt(3))
                current_on_lines = list(map(lambda value: value * current_nom, current_on_lines))
    
                title = 'Current On Lines At Maximal Grid Load'
    
                self.create_current_plot(x_vals=grid_lines, y_vals=current_on_lines, title=title,
                                         x_axis_label=x_label, y_axis_label=y_label)

    def create_voltage_plot_timeseries(self, x_vals=dict(), y_vals=dict(), title='title', x_axis_label='abscissa',
                                       y_axis_label='ordinate'):

        settings = self.__settings
        v_nom = 1 if settings.is_export_pu else settings.v_nom

        fig, voltage_axes = plt.subplots()

        # Spannungsband
        voltage_range_min = v_nom * 0.9
        voltage_range_max = v_nom * 1.1
        legend_entries = list()
        legend_entries.append(
            voltage_axes.axhline(voltage_range_max, color='r', linestyle='--', linewidth=1, label='Umax'))
        voltage_axes.axhline(voltage_range_min, color='r', linestyle='--', linewidth=1, label='Umin')

        if len(y_vals) < MAX_NUM_OF_NODES:

            x_vals = x_vals[TIMESTAMP]
            line_labels = ['$\pm$ 10 % ${U}_{ref}$']

            # min, max Y-Achse
            temp_y_min = float(max(y_vals[(list(y_vals.keys())[0])]))
            temp_y_max = float(min(y_vals[(list(y_vals.keys())[0])]))

            for key, value in y_vals.items():
                node_voltages = list(map(lambda voltage: float(voltage), value))
                node_voltages = list(map(lambda voltage: round(voltage, 3), node_voltages))
                legend_entries.append(voltage_axes.plot(x_vals, node_voltages, '-', linewidth=1, label=key)[0])
                line_labels.append(key)

                sub_y_min = min(node_voltages)
                sub_y_max = max(node_voltages)

                if sub_y_min < temp_y_min:
                    temp_y_min = sub_y_min
                if sub_y_max > temp_y_max:
                    temp_y_max = sub_y_max

        rel_max_delta = 1.07
        rel_min_delta = 1.03

        if temp_y_min < voltage_range_min:
            y_min = temp_y_min - (temp_y_max * (rel_min_delta - 1))
        else:
            y_min = voltage_range_min - (voltage_range_max * (rel_min_delta - 1))

        if temp_y_max < voltage_range_max:
            y_max = voltage_range_max * rel_max_delta
        else:
            y_max = temp_y_max * rel_max_delta

        voltage_axes.set_ylim(y_min, y_max)

        # Titel des Diagramms
        voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)

        # Y-Achsentitel
        voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)

        # X-Achsentitel
        voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)

        # X-Achsenbeschriftungen
        stepsize = 1 if len(x_vals) < 24 else len(x_vals) / 8
        voltage_axes.set_xticks(np.arange(0, len(x_vals), stepsize))
        plt.xticks(rotation=45)
        plt.grid(True, linewidth=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.18)
        voltage_axes.legend(legend_entries, line_labels, loc="upper right", borderaxespad=0.3, fancybox=True,
                            prop={'size': 8})
        file_name = str(title + IMG_FILE_EXTENSION)
        file_path_name = os.path.join(PLOT_EXPORT_PATH, file_name)
        plt.savefig(file_path_name, format='png', dpi=120)
        plt.clf()
        plt.cla()

    def create_current_plot_timeseries(self, x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                                       y_axis_label="ordinate"):
        settings = self.__settings
        v_nom, s_nom = (settings.v_nom, settings.s_nom) if settings.is_export_pu else (1, 1)
        current_nom = s_nom / v_nom
        fig, current_axes = plt.subplots()

        # Stromrange
        current_range_max = (s_nom / (v_nom * math.sqrt(3))) * 1.1

        legend_entries = list()

        if len(y_vals) < MAX_NUM_OF_NODES:

            x_vals = x_vals[TIMESTAMP]

            # max Y-Achse
            temp_y_max = float(min(y_vals[(list(y_vals.keys())[0])]))
            line_labels = list()

            for key, value in y_vals.items():
                line_currents = list(map(lambda current: float(current) * current_nom, value))
                line_currents = list(map(lambda current: round(current, 3), line_currents))
                legend_entries.append(current_axes.plot(x_vals, line_currents, '-', linewidth=1, label=key)[0])
                line_labels.append(key)

                sub_y_max = max(line_currents)

                if sub_y_max > temp_y_max:
                    temp_y_max = sub_y_max

        rel_max_delta = 1.07

        if temp_y_max < current_range_max:
            y_max = current_range_max * rel_max_delta
        else:
            y_max = temp_y_max * rel_max_delta

        current_axes.set_ylim(0, y_max)

        # Titel des Diagramms
        current_axes.set_title(title, fontsize=TITLE_FONTSIZE)

        # Y-Achsentitel
        current_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)

        # X-Achsentitel
        current_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)

        # X-Achsenbeschriftungen
        stepsize = 1 if len(x_vals) < 24 else len(x_vals) / 8
        current_axes.set_xticks(np.arange(0, len(x_vals), stepsize))
        plt.xticks(rotation=45)
        plt.grid(True, linewidth=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.18)
        current_axes.legend(legend_entries, line_labels, loc="upper right", borderaxespad=0.3, fancybox=True,
                            prop={'size': 8})
        file_name = str(title + IMG_FILE_EXTENSION)
        file_path_name = os.path.join(PLOT_EXPORT_PATH, file_name)
        plt.savefig(file_path_name, format='png', dpi=120)
        plt.clf()
        plt.cla()

    def create_voltage_plot(self, x_vals=dict(), y_vals=dict(), title="title", x_axis_label="abscissa",
                            y_axis_label="ordinate"):

        settings = self.__settings
        v_nom = 1 if settings.is_export_pu else settings.v_nom
        fig, voltage_axes = plt.subplots()

        # Spannungsband
        voltage_range_min = v_nom * 0.9
        voltage_range_max = v_nom * 1.1
        voltage_axes.axhline(voltage_range_max, color='r', linestyle='--', label='Umax')
        voltage_axes.axhline(voltage_range_min, color='r', linestyle='--', label='Umin')

        # Balkendiagramm erstellen
        volt_rects = voltage_axes.bar(x_vals, y_vals, width=0.5, label='Nodevoltage', color='#0090ff')

        # Titel des Diagramms
        voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)

        # Y-Achsentitel
        voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)

        # min, max Y-Achse
        temp_y_min = min(y_vals)
        temp_y_max = max(y_vals)
        rel_max_delta = 1.1

        if temp_y_min < voltage_range_min:
            y_min = temp_y_min - (temp_y_max * (rel_max_delta - 1))
        else:
            y_min = voltage_range_min - (voltage_range_max * (rel_max_delta - 1))

        if temp_y_max < voltage_range_max:
            y_max = voltage_range_max * rel_max_delta
        else:
            y_max = temp_y_max * rel_max_delta

        voltage_axes.set_ylim(y_min, y_max)

        # X-Achsentitel
        voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)

        # X-Achsenbeschriftungen
        voltage_axes.set_xticks(x_vals)

        # absolute max. Werte der einzelnen Balken
        self.autolabel(volt_rects, voltage_axes, 3)

        labels = ['$\pm$ 10 % ${U}_{ref}$', 'voltage at nodes']
        handles, _ = voltage_axes.get_legend_handles_labels()

        # Slice list to remove first handle
        voltage_axes.legend(handles=handles[1:], labels=labels)
        plt.grid(True, linewidth=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.18)
        file_name = str(title + IMG_FILE_EXTENSION)
        file_path_name = os.path.join(PLOT_EXPORT_PATH, file_name)
        plt.savefig(file_path_name, format='png', dpi=120)
        plt.clf()
        plt.cla()

    def create_current_plot(self, x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                            y_axis_label="ordinate"):

        fig, voltage_axes = plt.subplots()

        # Balkendiagramm erstellen
        volt_rects = voltage_axes.bar(x_vals, y_vals, width=0.5, label='Current', color='#ff8a00')

        # Titel des Diagramms
        voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)

        # Y-Achsentitel
        voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)

        # min, max Y-Achse
        temp_y_min = min(y_vals)
        temp_y_max = max(y_vals)
        rel_max_delta = 1.1

        y_min = 0
        y_max = temp_y_max * rel_max_delta

        voltage_axes.set_ylim(y_min, y_max)

        # X-Achsentitel
        voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)

        # X-Achsenbeschriftungen
        voltage_axes.set_xticks(x_vals)

        # absolute max. Werte der einzelnen Balken
        self.autolabel(volt_rects, voltage_axes, 0)

        voltage_axes.legend()
        plt.grid(True, linewidth=0.3)
        plt.subplots_adjust(left=0.15, bottom=0.18)
        file_name = str(title + IMG_FILE_EXTENSION)
        file_path_name = os.path.join(PLOT_EXPORT_PATH, file_name)
        plt.savefig(file_path_name, format='png', dpi=120)
        plt.clf()
        plt.cla()

    def autolabel(self, rects, axes, decimals=2, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0, 'right': 1, 'left': -1}

        for rect in rects:
            if decimals == 0:
                height = int(round(float(rect.get_height())))
            else:
                height = round(float(rect.get_height()), decimals)
            axes.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                          xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                          textcoords="offset points",  # in both directions
                          ha=ha[xpos], va='bottom')
