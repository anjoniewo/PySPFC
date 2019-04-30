from gridelementparser import GridElementParser
from gridnode import GridNode


# Parser-Klasse zum Einleser der Leitungsdaten
class GridNodeParser(GridElementParser):
	
	def __init__(self, file_path):
		
		super(GridNodeParser, self).__init__()
		
		self.node_parameters = []
		
		file_path = "C:\\Users\\EUProjekt\\Desktop\\AnjoNie\\02_Projekte\\LoadFlowSimulationTool\\" + str(
			file_path) + str(".csv")
		
		self.read_node_parameters(file_path)
		self.get_nodes_from_csv_dictionary()
	
	def read_node_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
		
	def get_nodes_from_csv_dictionary(self):
		
		parameter_list = []
		gridnode_list = []
		
		list_of_keys = list(self.csv_dictionary.keys())
		
		# wenn das csv dictionary nicht leer ist
		if list_of_keys:
			number_of_gridnodes = len(self.csv_dictionary[list_of_keys[0]])
			
			# alle Eintraege des dictionaries durchgehen
			for i in range(0, number_of_gridnodes):
				for key in self.csv_dictionary:
					if key == "name":
						gridnode_name = self.csv_dictionary[key][i]
					elif key == "typenumber":
						type_number = self.csv_dictionary[key][i]
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
				
				gridnode = GridNode(gridnode_name, type_number, parameter_list)
				gridnode_list.append(gridnode)
		
		s = ""
		
		
				
		
	
	
nodeparser = GridNodeParser("gridnodes")