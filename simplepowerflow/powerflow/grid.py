from simplepowerflow.powerflow.csvexport import CSVexport
from simplepowerflow.powerflow.csvimport import CSVimport
from simplepowerflow.powerflow.griddataexport.electrical_schematic import create_network_schematic
from simplepowerflow.powerflow.griddataexport.export_gridline_data import export_data_to_csv
from simplepowerflow.powerflow.gridelements.busadmittancematrix import BusAdmittanceMatrix
from simplepowerflow.powerflow.gridelements.gridline import GridLine
from simplepowerflow.powerflow.gridelements.gridnode import GridNode
from simplepowerflow.powerflow.powerflow.jacobianmatrix import JacobianMatrix
from simplepowerflow.powerflow.powerflow.powerflow import PowerFlow
from simplepowerflow.powerflow.powerflow.powerflowreporter import LoadFlowReporter


class Grid:
	"""
	the main class to perform imports of network data and powerflow calculations
	"""
	
	# Initialisierungskonstruktor
	def __init__(self):
		
		"""
		definition of class attributes and initializing with default values
		"""
		self.__v_nom = 0.4
		self.__s_nom = 630
		
		# name of slack node, defined in simulation_settings.csv
		self.__slack_node = None
		
		# Liste von Knoten und Liste von Leitungen
		self.__grid_node_list = list()
		self.__grid_line_list = list()
		
		# Liste von Transformatoren im Netz
		self.__transformer_list = list()
		
		self.bus_admittance_matrix = None
		self.jacobi_matrix = None
		self.powerflow = None
		
		self.timestamps = None
		
		self.grid_node_results = dict()
		self.grid_line_results = dict()
		
		# Instanzierung der LoadFlowReporter-Klasse
		self.load_flow_reporter = LoadFlowReporter()
	
	# getter
	def get_grid_node_list(self):
		return self.__grid_node_list
	
	def get_grid_line_list(self):
		return self.__grid_line_list
	
	def get_transformers(self):
		return self.__transformer_list
	
	def import_csv_data(self):
		csv_import = CSVimport()
		csv_import.import_csv_files()
		self.__grid_node_list = csv_import.grid_nodes
		self.__grid_line_list = csv_import.grid_lines
		self.__slack_node = csv_import.network_settings.slack
		self.__v_nom = csv_import.network_settings.v_nom
		self.__s_nom = csv_import.network_settings.s_nom
		self.timestamps = csv_import.time_stamp_keys
		self.create_bus_admittance_matrix()
	
	def create_bus_admittance_matrix(self):
		# Instanzierung der BusAdmittanceMatrix-Klasse
		self.bus_admittance_matrix = BusAdmittanceMatrix(self.__grid_node_list, self.__grid_line_list,
		                                                 self.__transformer_list)
	
	# Methode erstellt einen neuen Netzknoten und fuegt diesen der Knotenliste hinzu
	def create_grid_node(self, name, type, node_parameters):
		# Instanzierung eines neuen GridNode Objektes
		node = GridNode(name, type, node_parameters)
		self.add_grid_node(node)
	
	# Methode fuegt der Netzknotenliste einen Knoten hinzu
	def add_grid_node(self, grid_node):
		self.__grid_node_list.append(grid_node)
	
	# Methode erstellt einen neuen Netzzweig und fuegt diese der Leitungsliste hinzu
	def create_grid_line(self, node_i, node_j, line_parameters):
		# Instanzierung eines neuen GridNode Objektes
		line = GridLine(node_i, node_j, line_parameters)
		self.add_grid_line(line)
	
	# Methode fuegt der Leitungsliste einen Netzzweig hinzu
	def add_grid_line(self, grid_line):
		self.__grid_line_list.append(grid_line)
	
	# Gibt alle Knoten des Netzes in der Konsole aus
	def print_grid_node_list(self):
		if not len(self.__grid_node_list):
			print("\nKeine Knoten in Liste")
		else:
			for i in range(0, len(self.__grid_node_list)):
				print(self.__grid_node_list[i])
	
	# Gibt alle Knoten des Netzes in der Konsole aus
	
	def print_grid_line_list(self):
		if not len(self.__grid_line_list):
			print("\nKeine Leitungen in Liste")
		else:
			for i in range(0, len(self.__grid_line_list)):
				print(self.__grid_line_list[i])
	
	# Methode gibt die aktuelle Knotenadmittanzmatrix zurück
	def get_bus_admittance_matrix(self):
		return self.bus_admittance_matrix.matrix
	
	# Inverse der Knotenadmittanzmatrix berechnen
	def get_inverse_of_bus_admittance_matrix(self):
		return self.__bus_admittance_matrix.calc_inverse()
	
	# Lastflussberechnung durchfuehren
	def do_powerflow(self):
		"""
		Methods calls the do_powerflow() method of the PowerFlow class after
		:return:
		"""
		for timestamp in self.timestamps:
			gridnodes, voltagenodes = self.prepare_data_for_powerflow(timestamp=timestamp)
			
			self.jacobi_matrix = JacobianMatrix(gridnodes=gridnodes, voltagenodes=voltagenodes,
			                                    bus_admittance_matrix=self.bus_admittance_matrix.matrix)
			
			self.powerflow = PowerFlow(v_nom=self.__v_nom, s_nom=self.__s_nom,
			                           bus_admittance_matrix=self.bus_admittance_matrix.matrix,
			                           jacobimatrix=self.jacobi_matrix, gridnodes=gridnodes,
			                           gridlines=self.__grid_line_list, transformers=self.__transformer_list)
			
			self.grid_node_results[timestamp], self.grid_line_results[timestamp] = self.powerflow.do_powerflow()
	
	def prepare_data_for_powerflow(self, timestamp):
		"""
		Method prepares time variant data to perform a powerflow calculation of a single timestamp
		:return:
		"""
		gridnodes = list()
		voltagenodes = list()
		for gridnode in self.__grid_node_list:
			sum_of_p_max = 0
			sum_of_p_min = 0
			sum_of_q_max = 0
			sum_of_q_min = 0
			sum_of_active_power_gen = 0
			sum_of_reactive_power_gen = 0
			sum_of_active_power_load = 0
			sum_of_reactive_power_load = 0
			if len(gridnode.generators):
				for generator in gridnode.generators:
					sum_of_p_max += generator.p_max
					sum_of_p_min += generator.p_min
					sum_of_q_max += generator.q_max
					sum_of_q_min += generator.q_min
					sum_of_active_power_gen += generator.series_data[timestamp]['P']
					sum_of_reactive_power_gen += generator.series_data[timestamp]['Q']
			if len(gridnode.loads):
				for load in gridnode.loads:
					sum_of_active_power_load += load.series_data[timestamp]['P']
					sum_of_reactive_power_load += load.series_data[timestamp]['Q']
			
			p_load_pu = sum_of_active_power_load / self.__s_nom
			q_load_pu = sum_of_reactive_power_load / self.__s_nom
			
			# transform to slack node
			if gridnode.name == self.__slack_node:
				v_mag_pu = self.__v_nom / self.__v_nom
				v_angle = 0
				p_max_pu = self.__s_nom / self.__s_nom
				p_min_pu = self.__s_nom / self.__s_nom
				q_max_pu = self.__s_nom / self.__s_nom
				q_min_pu = self.__s_nom / self.__s_nom
				typenumber = gridnode.get_grid_node_type_index_of('slack')
				gridnode = GridNode(gridnode.name, v_mag=v_mag_pu, v_angle=v_angle, p_load=p_load_pu, q_load=q_load_pu,
				                    typenumber=typenumber, p_max=p_max_pu, p_min=p_min_pu, q_max=q_max_pu,
				                    q_min_pu=q_min_pu)
				gridnodes.append(gridnode)
				voltagenodes.append(gridnode)
			# transform to a PV node
			elif sum_of_active_power_gen:
				v_mag_pu = self.__v_nom / self.__v_nom
				p_gen_pu = sum_of_active_power_gen / self.__s_nom
				p_max_pu = sum_of_p_max / self.__s_nom
				p_min_pu = sum_of_p_min / self.__s_nom
				q_max_pu = sum_of_q_max / self.__s_nom
				q_min_pu = sum_of_q_min / self.__s_nom
				typenumber = gridnode.get_grid_node_type_index_of('PV')
				gridnode = GridNode(gridnode.name, p_gen=p_gen_pu, v_mag=v_mag_pu, p_load=p_load_pu, q_load=q_load_pu,
				                    p_min=p_min_pu, p_max=p_max_pu, q_min=q_min_pu, q_max=q_max_pu,
				                    typenumber=typenumber)
				gridnodes.append(gridnode)
				voltagenodes.append(gridnode)
			# transform to a PQ node
			else:
				gridnode = GridNode(gridnode.name, p_gen=0, q_gen=0, p_load=p_load_pu, q_load=q_load_pu,
				                    typenumber=gridnode.get_grid_node_type_index_of('PQ'))
				gridnodes.append(gridnode)
		
		return gridnodes, voltagenodes
	
	def export_powerflow_results(self):
		"""

		:param csv_export_path: export directory for powerflow results
		:return: -
		"""
		csv_export = CSVexport()
		csv_export.export_grid_node_results(self.timestamps, self.grid_node_results)
		csv_export.export_grid_line_results(self.timestamps, self.grid_line_results)
		
		# create network schematic for PDF report
		create_network_schematic(self.__grid_line_list, self.__transformer_list)
	
	# self.export_node_voltage_plot()
	# self.export_currents_on_lines_plot()
	
	def print_loadflow_results(self):
		if self.powerflow.grid_node_results:
			print(self.powerflow)
		else:
			print("Lastflussberechnung wurde noch nicht durchgefuehrt!")
	
	# Methode gibt die aktuelle Knotenadmittanzmatrix zurück
	def print_bus_admittance_matrix(self):
		"""
		Method prints busadmittance matrix in console
		:return: -
		"""
		result = ""
		matrix = self.bus_admittance_matrix.matrix
		n = len(matrix)
		for i in range(0, n):
			for j in range(0, n):
				element = matrix[i][j]
				if element.get_real_part() == 0 and element.get_imaginary_part() == 0:
					result += "{0:^50}".format("0")
				elif element.get_imaginary_part() < 0:
					result += "{0:^50}".format(
						str(element.get_real_part()) + " - j(" + str(element.get_imaginary_part() * -1) + ")")
				else:
					result += "{0:^50}".format(
						str(element.get_real_part()) + " + j(" + str(element.get_imaginary_part()) + ")")
			
			result += "\n"
		print("")
		print(result)
