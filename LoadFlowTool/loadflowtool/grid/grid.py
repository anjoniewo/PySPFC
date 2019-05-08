from LoadFlowTool.loadflowtool.grid.busadmittancematrix import BusAdmittanceMatrix
from LoadFlowTool.loadflowtool.grid.gridline import GridLine
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode
from LoadFlowTool.loadflowtool.loadflow.loadflowreporter import LoadFlowReporter


# Klasse fuer ein elektrisches Netz
class Grid:
	
	# Initialisierungskonstruktor
	def __init__(self, frequency=50, grid_node_list=list(), grid_line_list=list()):
		
		# Netzfrequenz (default 50 Hz)
		self.__frequency = frequency
		
		# Liste von Knoten und Liste von Leitungen
		self.__grid_node_list = grid_node_list
		self.__grid_line_list = grid_line_list
		
		# Instanzierung der LoadFlowReporter-Klasse
		self.load_flow_reporter = LoadFlowReporter()
		
		# Instanzierung der BusAdmittanceMatrix-Klasse
		self.__bus_admittanz_matrix = BusAdmittanceMatrix()
	
	# getter
	def get_frequency(self):
		return self.__frequency
	
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
		line = GridLine(self.__frequency, node_i, node_j, line_parameters)
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
	
	# Methode zur Berechnung der aktuellen Knotenadmittanz-Matrix
	# Übergabeparameter: Knotenliste [grid_node_list], Admittanzenliste (Gridline-Liste) [grid_line_list]
	def calc_bus_admittance_matrix(self):
		self.__bus_admittanz_matrix.calc_matrix(self.__grid_node_list, self.__grid_line_list)
	
	# Methode gibt die aktuelle Knotenadmittanzmatrix zurück
	def get_bus_admittance_matrix(self):
		return self.__bus_admittanz_matrix.matrix
	
	# Inverse der Knotenadmittanzmatrix berechnen
	def get_inverse_of_bus_admittance_matrix(self):
		return self.__bus_admittanz_matrix.calc_inverse()
		
	
	# Methode gibt die aktuelle Knotenadmittanzmatrix zurück
	def print_bus_admittance_matrix(self):
		result = ""
		matrix = self.__bus_admittanz_matrix.matrix
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
		
		print(result)
