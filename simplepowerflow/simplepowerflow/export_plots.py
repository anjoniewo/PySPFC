import matplotlib.pyplot as plt
import numpy as np

from simplepowerflow.simplepowerflow.csvexport import MAX_NUM_OF_NODES, TITLE_FONTSIZE, LABEL_FONTSIZE, PLOT_EXPORT_PATH


class Plotter:
    def __init__(self, settings):
        self.__settings = settings

    def export_currents_on_lines_plot(self, grid_line_results):
        """
        calls create_current_plot() with specified parameters
        """

        if grid_line_results['timestamp']:
            timestamps = dict([(key, value) for key, value in grid_line_results.items() if key == 'timestamp'])
            del grid_line_results['timestamp']
            line_currents = grid_line_results

            title = 'Current on lines'
            x_label = 'Time \u2192'
            y_label = 'Current in pu \u2192' if self.__settings.is_export_pu else 'Current in A \u2192'

            self.create_current_plot(timestamps, line_currents, title=title, x_axis_label=x_label, y_axis_label=y_label)

    def export_node_voltage_plot(self, grid_node_results):
        """
        calls create_voltage_plot() with specified parameters
        """

        node_voltages = dict()

        if grid_node_results['timestamp']:
            timestamps = dict([(key, value) for key, value in grid_node_results.items() if key == 'timestamp'])
            del grid_node_results['timestamp']
            node_voltages = grid_node_results

            title = "Bus voltage"
            x_label = "Time \u2192"
            y_label = "Voltage in pu \u2192" if self.__settings.is_export_pu else "Voltage in kV \u2192"

        self.create_voltage_plot(timestamps, node_voltages, title=title, x_axis_label=x_label, y_axis_label=y_label)

    def create_voltage_plot(self, x_vals=dict(), y_vals=dict(), title="title", x_axis_label="abscissa",
                            y_axis_label="ordinate"):

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

            x_vals = x_vals['timestamp']
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

        plt.subplots_adjust(left=0.15, bottom=0.18)
        voltage_axes.legend(legend_entries, line_labels, loc="upper right", borderaxespad=0.3, fancybox=True,
                            prop={'size': 8})
        plt.savefig(PLOT_EXPORT_PATH + '\\' + title + '.png', format='png', dpi=120)
        plt.clf()
        plt.cla()

    def create_current_plot(self, x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                            y_axis_label="ordinate"):
        settings = self.__settings
        v_nom, s_nom = (1, 1) if settings.is_export_pu else (settings.v_nom, settings.s_nom)
        fig, current_axes = plt.subplots()

        # Stromrange
        current_range_max = (s_nom / v_nom) * 1.1

        legend_entries = list()

        if len(y_vals) < MAX_NUM_OF_NODES:

            x_vals = x_vals['timestamp']

            # max Y-Achse
            temp_y_max = float(min(y_vals[(list(y_vals.keys())[0])]))
            line_labels = list()

            for key, value in y_vals.items():
                line_currents = list(map(lambda voltage: float(voltage), value))
                line_currents = list(map(lambda voltage: round(voltage, 3), line_currents))
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

        plt.subplots_adjust(left=0.15, bottom=0.18)
        current_axes.legend(legend_entries, line_labels, loc="upper right", borderaxespad=0.3, fancybox=True,
                            prop={'size': 8})
        plt.savefig(PLOT_EXPORT_PATH + '\\' + title + '.png', format='png', dpi=120)
        plt.clf()
        plt.cla()
