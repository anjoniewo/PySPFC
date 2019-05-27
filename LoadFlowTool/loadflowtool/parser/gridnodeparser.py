# Parser-Klasse zum Einleser der Leitungsdaten
from LoadFlowTool.loadflowtool.parser.csvparser import CSVParser
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode


class GridNodeParser(CSVParser):
	
	def __init__(self, file_path):
		
		super(GridNodeParser, self).__init__()
		
		self.__gridnodes = list()
		
		self.__read_node_parameters(file_path)
		self.__get_nodes_from_csv_dictionary()
	
	# self.__grid_node_types = {"slack": 1, "load": 2, "voltage": 3}
	
	# getter
	# def get_grid_node_type_index_of(self, node_type):
	#     return self.__grid_node_types[node_type]
	
	def get_gridnodes(self):
		return self.__gridnodes
	
	def __read_node_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
	
	def __get_nodes_from_csv_dictionary(self):
		
		list_of_keys = list(self.csv_dictionary.keys())
		
		# wenn das csv dictionary nicht leer ist
		if list_of_keys:
			number_of_gridnodes = len(self.csv_dictionary[list_of_keys[0]])
			
			# alle Eintraege des dictionaries durchgehen
			for i in range(number_of_gridnodes):
				parameter_list = list()
				for key in self.csv_dictionary:
					if key == "name":
						gridnode_name = self.csv_dictionary[key][i]
					elif key == "typenumber":
						type_number = int(self.csv_dictionary[key][i])
					elif key == "p_load":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "q_load":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "p_injection":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "q_injection":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "theta in rad":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "node_voltage":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "p_min in MW":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "p_max in MW":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "q_min in MVar":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "q_max in MVar":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "s_nom in MVA":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "u_nom in kV":
						parameter_list.append(self.csv_dictionary[key][i])
				
				grid_node_parameters = self.__get_node_parameters_by_type(type_number, parameter_list)
				gridnode = GridNode(gridnode_name, type_number, grid_node_parameters)
				self.__gridnodes.append(gridnode)
	
	def __get_node_parameters_by_type(self, type_number, list_of_parameters):
		
		# list_of_parameters
		# [0] : p_load
		# [1] : q_load
		# [2] : p_injection
		# [3] : q_injection
		# [4] : theta
		# [5] : node_voltage
		# [6] : p_min
		# [7] : p_max
		# [8] : q_min
		# [9] : q_max
		# [10] : s_nom
		# [11] : u_nom
		
		# Konvertiere explizit Eingabeparameter String => Float
		for index, parameter in enumerate(list_of_parameters):
			if (type(parameter) == str) and (len(parameter)):
				list_of_parameters[index] = float(parameter)
		
		grid_node_parameters = list()
		# active_load_power
		grid_node_parameters.append(list_of_parameters[0])
		# reactive_load_power
		grid_node_parameters.append(list_of_parameters[1])
		# active_injection_power
		grid_node_parameters.append(list_of_parameters[2])
		# reactive_injection_power
		grid_node_parameters.append(list_of_parameters[3])
		# theta in rad
		grid_node_parameters.append(list_of_parameters[4])
		# node_voltage
		grid_node_parameters.append(list_of_parameters[5])
		# minimale Wirkleistungsgrenze
		grid_node_parameters.append(list_of_parameters[6])
		# maximale Wirkleistungsgrenze
		grid_node_parameters.append(list_of_parameters[7])
		# minimale Blindleistungsgrenze
		grid_node_parameters.append(list_of_parameters[8])
		# maximale Blindleistungsgrenze
		grid_node_parameters.append(list_of_parameters[9])
		# nominelle Scheinleistung (Bezugsgroeße)
		grid_node_parameters.append(list_of_parameters[10])
		# nominelle Spannung (Bezugsgroeße)
		grid_node_parameters.append(list_of_parameters[11])
		
		return grid_node_parameters
