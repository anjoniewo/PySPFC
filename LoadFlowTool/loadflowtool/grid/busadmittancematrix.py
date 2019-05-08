import numpy as np
from LoadFlowTool.loadflowtool.grid.admittance import Admittance
import copy


# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:
	
	# Initialisierungskonstruktor
	def __init__(self):
		self.matrix = None
		
		# Gridlineliste (Leitungsliste)
		self.__grid_line_list = list()
	
	# Methode zur Aufsummierung aller Admittanzen an einem Knoten
	# Parameter:
	# Knotennamen,
	# [Optional] Modus: True|False (all_admittances), Wenn True: werden alle Laengs- und Queradmittanzen aufsummiert. Wenn False: werden nur die Längsadmittanzen aufsummiert (Queradmittanzen werden igoniert)
	# Rückgabewert: kummulierter Admittanzenwert
	# Quelle: E. Handschin, Elektrische Energieübertragungssysteme. Teil 1: Stationaerer Betriebszustand. Heidelberg: Hueting, 1983, Seite 51
	def __get_sum_of_grid_lines_on_node(self, node_name_i, node_name_j):
		
		# Summenadmittanz an Knoten i und entspricht einem Element der Knotenadmittanzmatrix (KAM)
		sum_admittance = Admittance(g=0, b=0)
		
		# Diagonalelement ?
		is_diag_elem = node_name_i == node_name_j
		
		for grid_line in self.__grid_line_list:
			
			# echte Kopie der Leitungsadmittanz erzeugen
			grid_line_admittance = copy.deepcopy(grid_line.get_admittance())
			
			# pruefen ob Leitung beide Knoten verbidnet
			is_connecting_i_j = grid_line.get_node_name_i() == node_name_i and \
			                    grid_line.get_node_name_j() == node_name_j or \
			                    grid_line.get_node_name_i() == node_name_j and \
			                    grid_line.get_node_name_j() == node_name_i
			
			if is_connecting_i_j:
				# Addiere Längsadmittanz von Gridline zur Summenadmittanz (für Diagonal- und Nichtdiagonal-Elemente der KAM)
				sum_admittance += grid_line_admittance
			
			# Prüfen ob Modus "alle Admittanzen" true ist und ob Queradmittanz in Gridline vorhanden
			elif is_diag_elem and grid_line.get_transverse_admittance_on_node():
				# Addiere Knoten-Queradmittanz von Gridline zur Summenadmittanz (nur für Nichtdiagonal-Elemente der KAM)
				grid_line_transverse_admittance = copy.deepcopy(grid_line.get_transverse_admittance_on_node())
				sum_admittance += grid_line_admittance + grid_line_transverse_admittance
		
		return sum_admittance if is_diag_elem else sum_admittance * -1
	
	# Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
	def calc_matrix(self, grid_node_list, grid_line_list):
		
		# quadratische Matrixdimension: nxn
		n = len(grid_node_list)
		
		# Erstellung eines nxn-dimensionalen Numpy-Arrays
		self.matrix = np.ndarray(shape=(n, n), dtype=object)
		
		for i in range(0, n):
			# Knotenname speichern
			gridnode_name_i = grid_node_list[i].get_name()
			
			# Setzen der gefilterten Leitungsliste
			grid_line_list_with_node_name_i = [grid_line for grid_line in grid_line_list if
			                                   grid_line.get_node_name_i() == gridnode_name_i or
			                                   grid_line.get_node_name_j() == gridnode_name_i]
			
			self.__grid_line_list = copy.deepcopy(grid_line_list_with_node_name_i)
			
			for j in range(i, n):
				gridnode_name_j = grid_node_list[j].get_name()
				
				self.matrix[i][j] = self.matrix[j][i] = self.__get_sum_of_grid_lines_on_node(gridnode_name_i,
				                                                                             gridnode_name_j)