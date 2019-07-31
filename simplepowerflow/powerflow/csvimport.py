import os

import math
import pandas as pd

from simplepowerflow.powerflow.gridelements.generator import Generator
from simplepowerflow.powerflow.gridelements.gridline import GridLine
from simplepowerflow.powerflow.gridelements.gridnode import GridNode
from simplepowerflow.powerflow.gridelements.load import Load
from simplepowerflow.powerflow.utils.config import get_file_names

csv_import_path = os.path.join(os.path.dirname(__file__), '..\\csv_import')
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
		self.import_logger = ImportLogger()
		self.validator = ImportValidator()
		self.df_import = dict()
		self.network_settings = None
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
		self.network_settings = self.get_settings()
		self.get_lines()
		self.get_nodes()
		self.check_consistency()
		self.get_time_stamp_keys()
	
	def check_consistency(self):
		"""
		methode validates the imported data
		check if:
			- all gridnodes are connected via gridlines
			- no admittances/impedances of the gridlines are singular
			- every gridnode has at least one generator or one load
			- all time stamps are identical
		:return:
		"""
		1
	
	def get_time_stamp_keys(self):
		"""
		method creates a list of time stamp keys
		:return:
		"""
		time_stamp_keys = None
		for grid_node in self.grid_nodes:
			if len(grid_node.generators):
				generator = next((x for x in grid_node.generators if len(x.series_data)), None)
				time_stamp_keys = generator.series_data
				break
			elif len(grid_node.loads):
				load = next((x for x in grid_node.loads if len(x.series_data)), None)
				time_stamp_keys = load.series_data
				break
		
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
			load = Load(name=load_name, node_i=grid_node_name)
			loads.append(load)
		
		self.set_loads_data(loads)
		
		return loads
	
	def get_generators(self):
		"""
		creates a list of generators
		:return:
		"""
		generator_file_df = self.df_import[file_names['generators']]
		generators = list()
		for row in generator_file_df.iterrows():
			row = row[1]
			generator_name = row['name'] if 'name' in row else 'name#'
			grid_node_name = row['node_i'] if 'node_i' in row else 'node#'
			p_min = row['p_min'] if not math.isnan(float(row['p_min'])) else 0
			p_max = row['p_max'] if not math.isnan(float(row['p_max'])) else 100
			q_min = row['q_min'] if not math.isnan(float(row['q_min'])) else 0
			q_max = row['q_max'] if not math.isnan(float(row['q_max'])) else 100
			generator = Generator(name=generator_name, node_i=grid_node_name, p_min=p_min, p_max=p_max, q_min=q_min,
			                      q_max=q_max)
			generators.append(generator)
		
		self.set_generators_data(generators)
		
		return generators
	
	def set_series_data(self, elements, p_series_df, q_series_df):
		"""
		get all time varying generator data
		:return: a dictionary with key = <elements name>
		value = dictionary with key = timestamp, value = {'P': <active power>, 'Q': <reactive power>}
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
		:return: a dictionary with key = <generator name>
		value = dictionary with key = timestamp, value = {'P': <active power>, 'Q': <reactive power>}
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
		self.validator.validate_columns(cols_gridnodes, node_file_columns)
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
				self.import_logger.error.append('\nProgram was aborted. Entries are missing in "lines.csv"')
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
		self.__slack = slack
		self.__v_nom = v_nom
		self.__s_nom = s_nom
		self.__time_stamp_format = time_stamp_format
	
	def __get_slack_node(self):
		return self.__slack
	
	def __get_s_nom(self):
		return self.__s_nom
	
	def __get_v_nom(self):
		return self.__v_nom
	
	def __get_tim_stamp_format(self):
		return self.__time_stamp_format
	
	slack = property(__get_slack_node)
	s_nom = property(__get_s_nom)
	v_nom = property(__get_v_nom)
	time_stamp_format = property(__get_tim_stamp_format)


class ImportLogger:
	"""
	logger class to log import states
	"""
	
	def __init__(self):
		self.error = list()
		self.warning = list()
