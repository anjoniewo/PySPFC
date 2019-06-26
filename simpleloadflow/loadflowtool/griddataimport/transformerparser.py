# Parser-Klasse zum Einleser der Leitungsdaten
from simpleloadflow.loadflowtool.griddataimport.csvparser import CSVParser
from simpleloadflow.loadflowtool.grid.transformer import Transformer


class TransformerParser(CSVParser):
	
	def __init__(self, file_path):
		super(TransformerParser, self).__init__()
		
		self.__transformers = list()
		
		self.__read_transformer_parameters(file_path)
		self.__get_transformers_from_csv_dictionary()
	
	# getter
	def get_transformers(self):
		return self.__transformers
	
	def __read_transformer_parameters(self, file_path):
		self.read_csv_to_dictionary(file_path)
	
	def __get_transformers_from_csv_dictionary(self):
		
		parameter_list = list()
		
		list_of_keys = list(self.csv_dictionary.keys())
		
		# wenn das csv dictionary nicht leer ist
		if list_of_keys:
			number_of_transformers = len(self.csv_dictionary[list_of_keys[0]])
			
			# alle Eintraege des dictionaries durchgehen
			for i in range(number_of_transformers):
				for key in self.csv_dictionary:
					if key == "name":
						name = self.csv_dictionary[key][i]
					elif key == "node_i":
						node_i = self.csv_dictionary[key][i]
					elif key == "node_j":
						node_j = self.csv_dictionary[key][i]
					elif key == "r":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "x":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "g":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "b":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "tap_ratio":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "phase_shift":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
					elif key == "s_n":
						parameter_list.append(
							None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
				
				transformer = Transformer(name, node_i, node_j, parameter_list)
				self.__transformers.append(transformer)
				parameter_list = list()
