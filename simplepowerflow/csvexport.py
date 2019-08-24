import csv
import math

from constants import *

MAX_NUM_OF_NODES = 100


class CSVexport:
    """
    class to export simplepowerflow2 results to csv files
    """

    def __init__(self, settings=None):
        self.__settings = settings

    def export_gridnode_results(self, timestamps, grid_node_results):

        """
        method exports node results to csv files in a specified directory (csv_export_path)
        :param csv_export_path:
        :return:
        """

        settings = self.__settings
        v_nom, s_nom = (1, 1) if settings.is_export_pu == 1 else (settings.v_nom, settings.s_nom)

        p_load = {TIMESTAMP: list()}
        q_load = {TIMESTAMP: list()}
        p_gen = {TIMESTAMP: list()}
        q_gen = {TIMESTAMP: list()}
        v_mag = {TIMESTAMP: list()}
        v_angle = {TIMESTAMP: list()}
        for timestamp in timestamps:
            p_load[TIMESTAMP].append(timestamp)
            q_load[TIMESTAMP].append(timestamp)
            p_gen[TIMESTAMP].append(timestamp)
            q_gen[TIMESTAMP].append(timestamp)
            v_mag[TIMESTAMP].append(timestamp)
            v_angle[TIMESTAMP].append(timestamp)
            timestamp_data = grid_node_results[timestamp]
            for key, value in timestamp_data.items():
                if key not in p_load:
                    p_load[key] = list()
                    q_load[key] = list()
                    p_gen[key] = list()
                    q_gen[key] = list()
                    v_mag[key] = list()
                    v_angle[key] = list()

                if 'p_load' in value:
                    p_load[key].append(str(value['p_load'] * s_nom))
                if 'q_load' in value:
                    q_load[key].append(str(value['q_load'] * s_nom))
                if 'p_gen' in value:
                    p_gen[key].append(str(value['p_gen'] * s_nom))
                if 'q_gen' in value:
                    q_gen[key].append(str(value['q_gen'] * s_nom))
                if 'v_magnitude' in value:
                    v_mag[key].append(str(value['v_magnitude'] * v_nom))
                if 'v_angle' in value:
                    v_angle[key].append(str(value['v_angle']))

        # data export to csv files
        self.export_data_to_csv(file_name="p_loads", data_dict=p_load)
        self.export_data_to_csv(file_name="q_loads", data_dict=q_load)
        self.export_data_to_csv(file_name='p_generators', data_dict=p_gen)
        self.export_data_to_csv(file_name='q_generators', data_dict=q_gen)
        self.export_data_to_csv(file_name='v_magnitudes', data_dict=v_mag)
        self.export_data_to_csv(file_name='v_angles', data_dict=v_angle)

        return v_mag

    def export_gridline_results(self, timestamps, grid_line_results):
        """
        method exports node results to csv files in a specified directory (csv_export_path)
        :param csv_export_path:
        :return:
        """

        settings = self.__settings
        v_nom, s_nom = (1, 1) if settings.is_export_pu == 1 else (settings.v_nom, settings.s_nom)
        current_nom = s_nom / (v_nom * math.sqrt(3))

        p_over_lines = {TIMESTAMP: list()}
        q_over_lines = {TIMESTAMP: list()}
        s_over_lines = {TIMESTAMP: list()}
        p_transmission_losses = {TIMESTAMP: list()}
        q_transmission_losses = {TIMESTAMP: list()}
        line_currents = {TIMESTAMP: list()}
        for timestamp in timestamps:
            p_over_lines[TIMESTAMP].append(timestamp)
            q_over_lines[TIMESTAMP].append(timestamp)
            s_over_lines[TIMESTAMP].append(timestamp)
            p_transmission_losses[TIMESTAMP].append(timestamp)
            q_transmission_losses[TIMESTAMP].append(timestamp)
            line_currents[TIMESTAMP].append(timestamp)
            timestamp_data = grid_line_results[timestamp]
            for key, value in timestamp_data.items():
                if key not in p_over_lines:
                    p_over_lines[key] = list()
                    q_over_lines[key] = list()
                    s_over_lines[key] = list()
                    p_transmission_losses[key] = list()
                    q_transmission_losses[key] = list()
                    line_currents[key] = list()

                if 'p_from_i_to_j' in value:
                    p_over_lines[key].append(str(value['p_from_i_to_j'] * s_nom))
                if 'q_from_i_to_j' in value:
                    q_over_lines[key].append(str(value['q_from_i_to_j'] * s_nom))
                if 's_from_i_to_j' in value:
                    s_over_lines[key].append(str(value['s_from_i_to_j'] * s_nom))
                if 'p_loss' in value:
                    p_transmission_losses[key].append(str(value['p_loss'] * s_nom))
                if 'q_loss' in value:
                    q_transmission_losses[key].append(str(value['q_loss'] * s_nom))
                if 'current_from_i_to_j' in value:
                    line_currents[key].append(str(value['current_from_i_to_j'] * current_nom))

        self.export_data_to_csv(file_name='p_lines', data_dict=p_over_lines)
        self.export_data_to_csv(file_name='q_lines', data_dict=q_over_lines)
        self.export_data_to_csv(file_name='s_lines', data_dict=s_over_lines)
        self.export_data_to_csv(file_name='p_transmission_losses', data_dict=p_transmission_losses)
        self.export_data_to_csv(file_name='q__transmission_losses', data_dict=q_transmission_losses)
        self.export_data_to_csv(file_name='current_on_lines', data_dict=line_currents)

        return line_currents

    def export_data_to_csv(self, file_name, data_dict):
        """
        exports data to csv file
        :param file_name:
        :param data_dict:
        :return:
        """
        file_name = str(file_name + CSV_FILE_EXTENSION)
        file_path_name = os.path.join(CSV_EXPORT_PATH, file_name)

        with open(file_path_name, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(data_dict.keys())
            writer.writerows(zip(*data_dict.values()))

            csvFile.close()


def autolabel(rects, axes, decimals=2, xpos='center'):
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
