from gridelementparser import GridElementParser
from gridnode import GridNode


# Parser-Klasse zum Einleser der Leitungsdaten
class GridNodeParser(GridElementParser):
	
	def __init__(self, file_path):
		
		super(GridNodeParser, self).__init__()
		
		self.gridnodes = list()
		
		file_path = "C:\\Users\\EUProjekt\\Desktop\\AnjoNie\\02_Projekte\\LoadFlowSimulationTool\\" + str(
			file_path) + str(".csv")
		
		self.read_node_parameters(file_path)
		self.get_nodes_from_csv_dictionary()
	
	def read_node_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
		
	def get_nodes_from_csv_dictionary(self):
		
		list_of_keys = list(self.csv_dictionary.keys())
		
		# wenn das csv dictionary nicht leer ist
		if list_of_keys:
			number_of_gridnodes = len(self.csv_dictionary[list_of_keys[0]])
			
			# alle Eintraege des dictionaries durchgehen
			for i in range(0, number_of_gridnodes):
				parameter_list = list()
				for key in self.csv_dictionary:
					if key == "name":
						gridnode_name = self.csv_dictionary[key][i]
					elif key == "typenumber":
						type_number = int(self.csv_dictionary[key][i])
					elif key == "active_load_power":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "reactive_load_power":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "active_injection_power":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "reactive_injection_power":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "theta":
						parameter_list.append(self.csv_dictionary[key][i])
					elif key == "node_voltage":
						parameter_list.append(self.csv_dictionary[key][i])
				
				gridnode = GridNode(gridnode_name, type_number, self.get_node_parameters_by_type(type_number, parameter_list))
				self.gridnodes.append(gridnode)
		
	def get_node_parameters_by_type(self, type_number, list_of_parameters):
		
		grid_node_parameters = list()
		grid_node_parameters.append(float(list_of_parameters[0]))
		grid_node_parameters.append(float(list_of_parameters[1]))
		
		if type_number == 0:
			# node_voltage
			grid_node_parameters.append(float(list_of_parameters[5]))
			# theta
			grid_node_parameters.append(float(list_of_parameters[4]))
		elif type_number == 2:
			# active_injection_power
			grid_node_parameters.append(float(list_of_parameters[2]))
			# node_voltage
			grid_node_parameters.append(float(list_of_parameters[5]))
		
		return grid_node_parameters