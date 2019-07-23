import os

import math
import pandas as pd

from simplepowerflow.powerflow.grid.generator import Generator
from simplepowerflow.powerflow.grid.gridline import GridLine
from simplepowerflow.powerflow.grid.gridnode import GridNode
from simplepowerflow.powerflow.grid.load import Load
from simplepowerflow.powerflow.utils.config import get_file_names

csv_import_path = os.path.join(os.path.dirname(__file__), '../../csv_import')
file_names = get_file_names()

cols_generators = ['name', 'node_i', 'p_max', 'p_min', 'q_max', 'q_min']
cols_gridnodes = ['name']
cols_lines = ['name', 'node_i', 'node_j', 'r', 'x', 'g_shunt', 'b_shunt', 'r_l', 'x_l', 'g_shunt_l', 'b_shunt_l',
              'length']
cols_loads = []
cols_settings = ['slack', 'v_nom', 's_nom', 'time_stamp_format']
cols_transformers = []

cols_generators_t_series = []
cols_loads_t_series = []


class CSVimport:
    """
        contains the parser methods for creating gridnode objects from imported csv dataframes
    """

    def __init__(self):
        self.validator = ImportValidator()
        self.df_import = dict()
        self.network_settings = None
        self.grid_lines = list()
        self.grid_nodes = list()

    def import_csv_files(self):
        """
            main method to call object creator submethods
        :return: none
        """
        self.import_files_as_dfs()
        self.network_settings = self.get_settings()
        self.get_lines()
        self.get_nodes()
        self.get_generators_series()
        self.get_loads_series()
        foo = 1

    def get_loads(self):
        load_file_df = self.df_import[file_names['loads']]
        loads = list()
        for row in load_file_df.iterrows():
            row = row[1]
            load_name = row['name']
            grid_node_name = row['node_i']
            load = Load(name=load_name, node_i=grid_node_name)
            loads.append(load)

        return loads

    def get_loads_series(self):
        loads = self.get_loads()
        loads_p_series_file_df = self.df_import[file_names['loads_p_series']]
        loads_q_series_file_df = self.df_import[file_names['loads_q_series']]
        if len(loads_p_series_file_df) == len(loads_q_series_file_df):
            p_q_series = dict(dict())
            for row in loads_p_series_file_df.iterrows():
                i = 0

    def get_generators(self):
        generator_file_df = self.df_import[file_names['generators']]
        generators = list()
        for row in generator_file_df.iterrows():
            row = row[1]
            generator_name = row['name']
            grid_node_name = row['node_i']
            p_min = row['p_min']
            p_max = row['p_max']
            q_min = row['q_min']
            q_max = row['q_max']
            generator = Generator(name=generator_name, node_i=grid_node_name, p_min=p_min, p_max=p_max, q_min=q_min,
                                  q_max=q_max)
            generators.append(generator)

        return generators

    def get_generators_series(self):
        generators = self.get_generators()
        generator_p_series_file_df = self.df_import[file_names['generators_p_series']]
        generator_q_series_file_df = self.df_import[file_names['generators_q_series']]
        if len(generator_p_series_file_df) == len(generator_q_series_file_df):
            p_q_series = dict(tuple())
            for row in generator_p_series_file_df.iterrows():
                i = 0

    def get_nodes(self):
        """
            get all gridnodes from the imported dataframes
        :return:
        """
        node_file_df = self.df_import[file_names['gridnodes']]
        node_file_columns = node_file_df.columns.values.tolist()
        self.validator.validate_columns(cols_gridnodes, node_file_columns)
        for row in node_file_df.iterrows():
            row = row[1]
            grid_node_name = row['name']
            grid_node = GridNode(grid_node_name)
            self.grid_nodes.append(grid_node)

    def get_lines(self):
        """
            get all the gridlines from the imported dataframes
        :return: none
        """
        line_file_df = self.df_import[file_names['lines']]
        line_file_columns = line_file_df.columns.values.tolist()
        self.validator.validate_columns(cols_lines, line_file_columns)
        for row in line_file_df.iterrows():
            row = row[1]
            grid_line_name = row['name']
            node_i = row['node_i']
            node_j = row['node_j']
            r_l = row['r_l'] if not math.isnan(row['r_l']) else None
            x_l = row['x_l'] if not math.isnan(row['x_l']) else None
            g_shunt_l = row['g_shunt_l'] if not math.isnan(row['g_shunt_l']) else 0
            b_shunt_l = row['b_shunt_l'] if not math.isnan(row['b_shunt_l']) else 0
            length = row['length'] if not math.isnan(row['length']) else None

            if not ((r_l or x_l) and length):
                print('\nProgram was aborted. Entries are missing in "lines.csv"')
                raise SystemExit(1)

            line_parameters = {'r_l': r_l, 'x_l': x_l, 'g_shunt_l': g_shunt_l, 'b_shunt_l': b_shunt_l, 'length': length}
            grid_line = GridLine(grid_line_name, node_i, node_j, line_parameters)
            self.grid_lines.append(grid_line)

    def get_settings(self):
        settings_file_df = self.df_import[file_names['sim_settings']]
        settings_file_columns = settings_file_df.columns.values.tolist()
        self.validator.validate_columns(cols_settings, settings_file_columns)
        slack = settings_file_df['slack'].iloc[0] if isinstance(settings_file_df['slack'].iloc[0], str) else None
        v_nom = settings_file_df['v_nom'].iloc[0] if not math.isnan(settings_file_df['v_nom'].iloc[0]) else None
        s_nom = settings_file_df['s_nom'].iloc[0] if not math.isnan(settings_file_df['s_nom'].iloc[0]) else None
        time_stamp_format = settings_file_df['time_stamp_format'].iloc[0] if isinstance(
            settings_file_df['time_stamp_format'].iloc[0], str) else None
        if not (slack and v_nom and s_nom and time_stamp_format):
            print('\nProgram was aborted. Entries are missing in "simulation_settings.csv"')
            raise SystemExit(1)

        return Settings(slack, v_nom, s_nom, time_stamp_format)

    def import_files_as_dfs(self):
        """
            imports all csv files from 'csv_import' path to dataframes
        :return:
        """
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
                self.df_import[file_name] = pd.read_csv(os.path.join(csv_import_path, file_name), delimiter=";")


class ImportValidator:
    """
        class for validating the imported csv-files
    """

    def __init__(self):
        pass

    def validate_series_data(self, data):
        1

    def validate_time_stamp_data(self):
        1

    def validate_columns(self, ref_columns, column_names):
        success = False

        nonexistent_cols = list()

        for col in column_names:
            if col not in ref_columns:
                nonexistent_cols.append(col)

        if len(nonexistent_cols):
            print('\nProgram was aborted. Following columns are missing:\n')
            print(nonexistent_cols)
            raise SystemExit(1)
        else:
            return success


class Settings:
    """
        imported settings from 'simulation_settings.csv' are saved in a Settings() object
    """

    def __init__(self, slack, v_nom=None, s_nom=None, time_stamp_format=None):
        self.slack = slack
        self.v_nom = v_nom
        self.s_nom = s_nom
        self.time_stamp_format = time_stamp_format


csv_import = CSVimport()
csv_import.import_csv_files()
