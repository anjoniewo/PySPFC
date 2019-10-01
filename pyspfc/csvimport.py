import math
import os

import pandas as pd

from pyspfc.config.fileconfig import get_file_names
from pyspfc.directories import get_import_path
from pyspfc.gridelements.generator import Generator
from pyspfc.gridelements.gridline import GridLine
from pyspfc.gridelements.gridnode import GridNode
from pyspfc.gridelements.load import Load

file_names = get_file_names()

cols_generators = ['name', 'node_i', 'p_max', 'p_min', 'q_max', 'q_min']
cols_gridnodes = ['name']
cols_lines = ['name', 'node_i', 'node_j', 'r_l', 'x_l', 'g_shunt_l', 'b_shunt_l', 'length']
cols_settings = ['slack', 'v_nom_kV', 's_nom_MVA', 'is_import_pu', 'is_export_pu', 'time_stamp_format']


class CSVimport:
    """
    contains the parser methods for creating gridnode objects from imported csv dataframes
    """

    def __init__(self):
        self.import_logger = ImportLogger()
        self.validator = ImportValidator()
        self.df_import = dict()
        self.simulation_settings = None
        self.grid_lines = list()
        self.grid_nodes = list()
        self.time_stamp_keys = list()

    def import_csv_files(self):
        """
        - main method to import all csv files from 'csv_import' folder
        - submethods create network elements and thus a network object
        :return: none
        """
        self.import_files_as_dfs()
        self.simulation_settings = self.get_settings()
        self.get_lines()
        self.get_nodes()
        self.get_time_stamp_keys()
        self.validator.check_consistency(self)

    def get_time_stamp_keys(self):
        """
        method creates a list of time stamp keys and sets it in the attribute self.time_stamp_keys
        :return: none
        """
        time_stamp_keys = None
        for grid_node in self.grid_nodes:
            if len(grid_node.generators):
                generator = next((x for x in grid_node.generators if len(x.p_q_series)), None)
                time_stamp_keys = generator.p_q_series
                break
            elif len(grid_node.loads):
                load = next((x for x in grid_node.loads if len(x.p_q_series)), None)
                time_stamp_keys = load.p_q_series
                break
            else:
                print('\nWARNING: Program was aborted. No generators neither loads are specified!\n')
                raise SystemExit(1)

        for key in time_stamp_keys:
            self.time_stamp_keys.append(key)

    def get_loads(self):
        """
        creates a list of loads
        :return:
        """
        load_file_df = self.df_import[file_names['loads']]
        loads = list()
        for row in load_file_df.iterrows():
            row = row[1]
            load_name = row['name']
            grid_node_name = row['node_i']
            load = Load(name=load_name, node=grid_node_name)
            loads.append(load)

        self.set_loads_data(loads)

        return loads

    def get_generators(self):
        """
        creates a list of generators
        :return: list of generators
        """
        settings = self.simulation_settings
        default_max = 1000 if settings.is_import_pu == 1 else settings.s_nom
        default_min = -1000 if settings.is_import_pu == 1 else float(settings.s_nom * -1)
        generator_file_df = self.df_import[file_names['generators']]
        generators = list()
        for row in generator_file_df.iterrows():
            row = row[1]
            generator_name = row['name'] if 'name' in row else 'name#'
            grid_node_name = row['node_i'] if 'node_i' in row else 'node#'
            p_min = row['p_min'] if not math.isnan(float(row['p_min'])) else default_min
            p_max = row['p_max'] if not math.isnan(float(row['p_max'])) else default_max
            q_min = row['q_min'] if not math.isnan(float(row['q_min'])) else default_min
            q_max = row['q_max'] if not math.isnan(float(row['q_max'])) else default_max
            generator = Generator(name=generator_name, node=grid_node_name, p_min=p_min, p_max=p_max, q_min=q_min,
                                  q_max=q_max)
            generators.append(generator)

        self.set_generators_data(generators)

        return generators

    @staticmethod
    def set_series_data(elements, p_series_df, q_series_df):
        """
        set all time varying generator data
        :return: none
        :param elements: list of objects, in this case either generators oder loads
        :param p_series_df: data frame with active power time series data
        :param q_series_df: data frame with reactive power time series data
        """
        for element in elements:
            time_stamps_p = p_series_df['time_stamp']
            time_stamps_q = q_series_df['time_stamp']
            elements_p_values = p_series_df[element.name]
            elements_q_values = q_series_df[element.name]

            values = dict()
            elements_data = dict(values)

            for index in range(len(time_stamps_p)):
                key = time_stamps_p[index]
                elements_data[key] = {'P': 0, 'Q': 0}
                elements_data[key]["P"] = elements_p_values[index]

            for index in range(len(time_stamps_q)):
                key = time_stamps_q[index]
                if key not in elements_data:
                    elements_data[key] = {'P': 0, 'Q': 0}

                elements_data[key]["Q"] = elements_q_values[index]

            element.set_p_q_series(elements_data)

    def set_generators_data(self, generators):
        """
        call of self.get_series_data with defined parameters
        :return: none
        :param generators: list of generator objects
        """
        generators_p_series_df = self.df_import[file_names['generators_p_series']]
        generators_q_series_df = self.df_import[file_names['generators_q_series']]
        self.set_series_data(generators, generators_p_series_df, generators_q_series_df)

    def set_loads_data(self, loads):
        """
        call of self.get_series_data with defined parameters
        :return: a dictionary with key = <load name>
        value = dictionary with key = timestamp, value = {'P': <active power>, 'Q': <reactive power>}
        """
        loads_p_series_df = self.df_import[file_names['loads_p_series']]
        loads_q_series_df = self.df_import[file_names['loads_q_series']]
        self.set_series_data(loads, loads_p_series_df, loads_q_series_df)

    def get_nodes(self):
        """
        get all gridnodes from the imported dataframes
        :return:
        """
        node_file_df = self.df_import[file_names['gridnodes']]
        node_file_columns = node_file_df.columns.values.tolist()
        self.validator.validate_columns(file_names['gridnodes'], cols_gridnodes, node_file_columns)
        for row in node_file_df.iterrows():
            row = row[1]
            grid_node_name = row['name']
            grid_node = GridNode(grid_node_name)
            self.grid_nodes.append(grid_node)

        generators = self.get_generators()
        loads = self.get_loads()

        for grid_node in self.grid_nodes:
            grid_node.set_generators([generator for generator in generators if generator.node == grid_node.name])
            grid_node.set_loads([load for load in loads if load.node == grid_node.name])

    def get_lines(self):
        """
            get all the gridlines from the imported dataframes
        :return: none
        """
        line_file_df = self.df_import[file_names['lines']]
        line_file_columns = line_file_df.columns.values.tolist()
        self.validator.validate_columns(file_names['lines'], cols_lines, line_file_columns)
        for row in line_file_df.iterrows():
            row = row[1]
            grid_line_name = row['name']
            node_i = row['node_i']
            node_j = row['node_j']

            if node_i == node_j:
                print('\nProgram was aborted. The following grid line has the same start and end bus:')
                print(grid_line_name)
                raise SystemExit(1)

            r_l = row['r_l'] if not math.isnan(row['r_l']) else None
            x_l = row['x_l'] if not math.isnan(row['x_l']) else None
            g_shunt_l = row['g_shunt_l'] if not math.isnan(row['g_shunt_l']) else 0
            b_shunt_l = row['b_shunt_l'] if not math.isnan(row['b_shunt_l']) else 0
            length = row['length'] if not math.isnan(row['length']) else None

            if not ((r_l or x_l) and length):
                self.import_logger.error.append('\nProgram was aborted. Entries are missing in "lines.csv"')
                print('\nProgram was aborted. Entries are missing in "lines.csv"')
                raise SystemExit(1)

            line_parameters = {'r_l': r_l, 'x_l': x_l, 'g_shunt_l': g_shunt_l, 'b_shunt_l': b_shunt_l, 'length': length}
            grid_line = GridLine(grid_line_name, node_i, node_j, line_parameters)
            self.grid_lines.append(grid_line)

    def get_settings(self):
        """
        parsing of the simulation settings
        :return: Settings() - object
        """
        settings_file_df = self.df_import[file_names['sim_settings']]
        settings_file_columns = settings_file_df.columns.values.tolist()

        # validation of column names
        self.validator.validate_columns(file_names['sim_settings'], cols_settings, settings_file_columns)

        slack = settings_file_df['slack'].iloc[0] if isinstance(settings_file_df['slack'].iloc[0], str) else None
        v_nom = settings_file_df['v_nom_kV'].iloc[0] if not math.isnan(settings_file_df['v_nom_kV'].iloc[0]) else None
        s_nom = settings_file_df['s_nom_MVA'].iloc[0] * 1000 if not math.isnan(
            settings_file_df['s_nom_MVA'].iloc[0]) else None
        is_import_pu = settings_file_df['is_import_pu'].iloc[0] if not math.isnan(
            settings_file_df['is_import_pu'].iloc[0]) else 0
        is_export_pu = settings_file_df['is_export_pu'].iloc[0] if not math.isnan(
            settings_file_df['is_export_pu'].iloc[0]) else 0
        time_stamp_format = settings_file_df['time_stamp_format'].iloc[0] if isinstance(
            settings_file_df['time_stamp_format'].iloc[0], str) else None
        if not (slack and v_nom and s_nom and time_stamp_format):
            print('\nProgram was aborted. Entries are missing in "simulation_settings.csv"')
            raise SystemExit(1)

        return Settings(slack, v_nom, s_nom, is_import_pu, is_export_pu, time_stamp_format)

    def import_files_as_dfs(self):
        """
            imports all csv files from default 'csv_import' path in the project root directory or from a specified
            directory
            @:param root_path
            all files will be imported an parsed into pandas dataframes
        :return: -
        """
        csv_import_path = get_import_path()
        assert os.path.isdir(csv_import_path), 'Path {} does not exist.'.format(csv_import_path)

        files = os.listdir(csv_import_path)
        nonexistent_files = list()

        for file_name in file_names.values():
            if file_name not in files:
                nonexistent_files.append(file_name)

        if len(nonexistent_files):
            print('\nProgram was aborted. Following files are missing:\n')
            print(nonexistent_files)
            raise SystemExit(1)
        else:
            for file_name in files:
                if file_name != 'export':
                    self.df_import[file_name] = pd.read_csv(os.path.join(csv_import_path, file_name), delimiter=";")


class ImportValidator:
    """
        class for validating the imported csv-files
    """

    def __init__(self):
        pass

    def check_consistency(self, csv_import):
        """
        methode validates the imported data
        check if:
            - all gridnodes are connected via gridlines
            - no admittances/impedances of the gridlines are singular
            - every gridnode has at least one generator or one load
            - all time stamps are identical
        :return: none
        """
        self.check_grid_nodes_are_connected(csv_import.grid_nodes, csv_import.grid_lines)
        self.check_grid_nodes_have_loads_or_generators(csv_import.grid_nodes)
        self.check_slack_in_settings_is_gridnode(csv_import.grid_nodes, csv_import.get_settings().slack)

    @staticmethod
    def check_grid_nodes_are_connected(grid_nodes, grid_lines):
        """
        method checks if all grid nodes are connected via grid lines
        :param grid_nodes: list of grid node objects
        :param grid_lines: list of grid line objects
        :return: none
        """

        grid_node_names = [grid_node.name for grid_node in grid_nodes]
        grid_nodes_i = [grid_line.get_node_name_i() for grid_line in grid_lines]
        grid_nodes_j = [grid_line.get_node_name_j() for grid_line in grid_lines]
        grid_nodes_from_lines = set(grid_nodes_i + grid_nodes_j)

        for grid_node_name in grid_node_names:
            if grid_node_name not in grid_nodes_from_lines:
                print('\nProgram was aborted. Following grid node is not connected: ')
                print(grid_node_name)
                raise SystemExit(1)

    @staticmethod
    def check_grid_nodes_have_loads_or_generators(grid_nodes):
        """
        method checks if every grid node has at least a generator or load element
        :param grid_nodes: list of grid nodes
        :return: none
        """
        for grid_node in grid_nodes:
            if not len(grid_node.generators) and not len(grid_node.loads):
                print('\nProgram was aborted. Following grid node has neither generators nor loads: ')
                print(grid_node.name)
                raise SystemExit(1)

    @staticmethod
    def check_slack_in_settings_is_gridnode(grid_nodes, slack_node_name):
        """
        method checks if every grid node has at least a generator or load element
        :param grid_nodes: list of grid nodes
        :return: none
        """
        if not slack_node_name in [grid_node.name for grid_node in grid_nodes]:
            print('\nProgram was aborted. Slack node in "simulation_settings.csv" was not defined in "gridnodes.csv"')
            print('Slack: ' + slack_node_name)
            raise SystemExit(1)

    @staticmethod
    def validate_columns(filename, ref_columns, column_names):
        """
        method validates if the column headings in the first row of a csv file corresponds to the default values
        :param filename: filename of the file to be validated
        :param ref_columns: default column headings
        :param column_names: actual column headings of the file
        :return:
        """
        success = False

        nonexistent_cols = list()

        for col in column_names:
            if col not in ref_columns:
                nonexistent_cols.append(col)

        if len(nonexistent_cols):
            print('\nProgram was aborted. Following columns are missing in:\n')
            print(filename)
            print(nonexistent_cols)
            raise SystemExit(1)
        else:
            return success


class Settings:
    """
        imported settings from 'simulation_settings.csv' are saved in a Settings() object
    """

    def __init__(self, slack, v_nom=None, s_nom=None, is_import_pu=None, is_export_pu=None, time_stamp_format=None):
        self.__slack = slack
        self.__v_nom = v_nom
        self.__s_nom = s_nom
        self.__is_import_pu = is_import_pu
        self.__is_export_pu = is_export_pu
        self.__time_stamp_format = time_stamp_format

    def __get_slack_node(self):
        return self.__slack

    def __get_s_nom(self):
        return self.__s_nom

    def __get_v_nom(self):
        return self.__v_nom

    def __get_is_import(self):
        return self.__is_import_pu

    def __get_is_export(self):
        return self.__is_export_pu

    def __get_tim_stamp_format(self):
        return self.__time_stamp_format

    slack = property(__get_slack_node)
    s_nom = property(__get_s_nom)
    v_nom = property(__get_v_nom)
    is_import_pu = property(__get_is_import)
    is_export_pu = property(__get_is_export)
    time_stamp_format = property(__get_tim_stamp_format)


class ImportLogger:
    """
    logger class to log import states
    """

    def __init__(self):
        self.error = list()
        self.warning = list()
