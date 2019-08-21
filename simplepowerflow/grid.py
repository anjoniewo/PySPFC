from simplepowerflow.csvexport import CSVexport
from simplepowerflow.csvimport import CSVimport
from simplepowerflow.electrical_schematic import create_network_schematic
from simplepowerflow.export_plots import Plotter
from simplepowerflow.export_results_to_pdf import create_pdf_report
from simplepowerflow.gridelements.busadmittancematrix import BusAdmittanceMatrix
from simplepowerflow.gridelements.gridline import GridLine
from simplepowerflow.gridelements.gridnode import GridNode
from simplepowerflow.powerflow.jacobianmatrix import JacobianMatrix
from simplepowerflow.powerflow.powerflow import PowerFlow
from simplepowerflow.powerflow.powerflowreporter import LoadFlowReporter


class Grid:
	"""
	the main class to perform imports of network data and simplepowerflow2 calculations
	"""
	
	# Initialisierungskonstruktor
	def __init__(self):
		
		"""
		definition of class attributes and initializing with default values
		"""
		
		self.__settings = None
		
		# Liste von Knoten und Liste von Leitungen
		self.__grid_node_list = list()
		self.__grid_line_list = list()
		
		# Liste von Transformatoren im Netz
		self.__transformer_list = list()
		
		self.bus_admittance_matrix = None
		self.jacobi_matrix = None
		self.powerflow = None
		
		self.timestamps = None
		
		self.gridnode_results = dict()
		self.gridline_results = dict()
		
		self.gridnode_results_for_pdf = dict()
		self.gridline_results_for_pdf = dict()
		
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
		"""
		imports grid data from 'csv_import' directory
		:return:
		"""
		csv_import = CSVimport()
		csv_import.import_csv_files()
		self.__grid_node_list = csv_import.grid_nodes
		self.__grid_line_list = csv_import.grid_lines
		self.__settings = csv_import.network_settings
		self.timestamps = csv_import.time_stamp_keys
		self.create_bus_admittance_matrix()
	
	def create_bus_admittance_matrix(self):
		"""
		instantiation of a BusAdmittanceMatrix object
		:return:
		"""
		
		settings = self.__settings
		
		if not settings.is_resistance_pu:
			# reference admittance value
			y_nom = (settings.s_nom / settings.v_nom ** 2)
			
			for index, gridline in enumerate(self.__grid_line_list):
				admittance = gridline.get_admittance()
				real_part_pu = admittance.get_real_part() / y_nom
				imag_part_pu = admittance.get_imaginary_part() / y_nom
				self.__grid_line_list[index].set_admittance(real_part_pu, imag_part_pu)
				
				transverse_admittance = gridline.get_transverse_admittance_on_node()
				real_part_pu = transverse_admittance.get_real_part() / y_nom
				imag_part_pu = transverse_admittance.get_imaginary_part() / y_nom
				self.__grid_line_list[index].set_transverse_admittance(real_part_pu, imag_part_pu)
		
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
			
			self.powerflow = PowerFlow(v_nom=self.__settings.v_nom, s_nom=self.__settings.s_nom,
			                           bus_admittance_matrix=self.bus_admittance_matrix.matrix,
			                           jacobimatrix=self.jacobi_matrix, gridnodes=gridnodes,
			                           gridlines=self.__grid_line_list, transformers=self.__transformer_list)
			
			self.gridnode_results[timestamp], self.gridline_results[timestamp] = self.powerflow.do_powerflow()
	
	def prepare_data_for_powerflow(self, timestamp):
		"""
		Method prepares time variant data to perform a simplepowerflow2 calculation of a single timestamp
		:return:
		"""
		
		settings = self.__settings
		v_nom, s_nom = (1, 1) if settings.is_import_pu else (settings.v_nom, settings.s_nom)
		
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
			
			p_load_pu = sum_of_active_power_load / s_nom
			q_load_pu = sum_of_reactive_power_load / s_nom
			
			# transform to slack node
			if gridnode.name == settings.slack:
				v_mag_pu = 1.0
				v_angle = 0.0
				p_max_pu = sum_of_p_max / s_nom
				p_min_pu = sum_of_p_min / s_nom
				typenumber = gridnode.get_grid_node_type_index_of('slack')
				gridnode = GridNode(gridnode.name, v_mag=v_mag_pu, v_angle=v_angle, p_load=p_load_pu, q_load=q_load_pu,
				                    typenumber=typenumber, p_max=p_max_pu, p_min=p_min_pu)
				gridnodes.append(gridnode)
				voltagenodes.append(gridnode)
			# transform to a PV node
			elif sum_of_active_power_gen:
				v_mag_pu = v_nom / v_nom
				p_gen_pu = sum_of_active_power_gen / s_nom
				p_max_pu = sum_of_p_max / s_nom
				p_min_pu = sum_of_p_min / s_nom
				q_max_pu = sum_of_q_max / s_nom
				q_min_pu = sum_of_q_min / s_nom
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

		:param csv_export_path: export directory for simplepowerflow2 results
		:return: -
		"""
		
		# save settings locally
		settings = self.__settings
		
		csv_export = CSVexport(settings)
		plotter = Plotter(settings)
		v_mag_data = csv_export.export_gridnode_results(self.timestamps, self.gridnode_results)
		line_currents = csv_export.export_gridline_results(self.timestamps, self.gridline_results)
		
		# filtered results for pdf report
		self.gridnode_results_for_pdf, self.gridline_results_for_pdf = self.get_worstcase_results()
		
		if len(self.gridnode_results_for_pdf) > 10:
			print("Number of grid nodes is significantly high. Readibility of plots might be bad.")
		
		# create result plots for node bus voltages and line currents
		plotter.export_node_voltage_plots(grid_node_timeseries_results=v_mag_data,
		                                  grid_node_min_max_results=self.gridnode_results_for_pdf)
		plotter.export_currents_on_lines_plots(grid_line_timeseries_results=line_currents,
		                                       grid_line_min_max_results=self.gridline_results_for_pdf)
		
		# create network schematic for PDF report
		create_network_schematic(self.__grid_line_list, self.__transformer_list)
	
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
	
	def create_pdf_report(self):
		"""
		method calls create_pdf_reporter() of export_results_to_pdf.py
		:return: -
		"""
		
		if len(self.gridnode_results_for_pdf) > 10:
			print("Number of grid nodes is significantly high. Readibility of PDF report might be bad.")
		
		settings = self.__settings
		create_pdf_report(self.gridnode_results_for_pdf, self.gridline_results_for_pdf, settings.v_nom, settings.s_nom)
	
	def get_worstcase_results(self):
		"""
		determine the timestamp with the highest or lowest voltage derivation of the reference voltage range
		:return:
		"""
		
		min_voltage = 1e20
		max_voltage = 0
		min_worstcase_timestamp = 0
		max_worstcase_timestamp = 0
		
		v_mag = {'timestamp': list()}
		for timestamp in self.timestamps:
			v_mag['timestamp'].append(timestamp)
			timestamp_data = self.gridnode_results[timestamp]
			for key, value in timestamp_data.items():
				if key not in v_mag:
					if 'v_magnitude' in value:
						temp_min_voltage = value['v_magnitude']
						temp_max_voltage = value['v_magnitude']
						if temp_min_voltage < min_voltage:
							min_voltage = temp_min_voltage
							min_worstcase_timestamp = timestamp
						if temp_max_voltage > max_voltage:
							max_voltage = temp_max_voltage
							max_worstcase_timestamp = timestamp
		
		min_worstcase = 'min'
		max_worstcase = 'max'
		min_max_gridnode_results = dict()
		min_max_gridline_results = dict()
		
		min_max_gridnode_results[min_worstcase] = self.gridnode_results[min_worstcase_timestamp]
		min_max_gridnode_results[max_worstcase] = self.gridnode_results[max_worstcase_timestamp]
		min_max_gridline_results[min_worstcase] = self.gridline_results[min_worstcase_timestamp]
		min_max_gridline_results[max_worstcase] = self.gridline_results[max_worstcase_timestamp]
		
		return min_max_gridnode_results, min_max_gridline_results
