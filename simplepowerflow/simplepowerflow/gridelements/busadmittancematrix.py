import copy

import numpy as np

from simplepowerflow.simplepowerflow.gridelements.admittance import Admittance
from simplepowerflow.simplepowerflow.gridelements.gridline import GridLine


# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:
	
	# Initialisierungskonstruktor
	def __init__(self, grid_node_list, grid_line_list, transformer_list):
		self.matrix = None
		
		# Gridlineliste (Leitungsliste)
		self.__bus_connecter_list = grid_line_list + transformer_list
		
		# Transformator-Liste
		self.__transformer_list = transformer_list
		
		self.calc_matrix(grid_node_list)
	
	def __get_sum_of_grid_lines_on_node(self, node_name_i, node_name_j):
		"""
		Methode zur Aufsummierung aller Admittanzen an einem Knoten
		Parameter:
		Knotennamen,
		[Optional] Modus: True|False (all_admittances), Wenn True: werden alle Laengs- und Queradmittanzen aufsummiert.
		Wenn False: werden nur die Längsadmittanzen aufsummiert (Queradmittanzen werden igoniert)
		Rückgabewert: kummulierter Admittanzenwert
		Quelle: E. Handschin, Elektrische Energieübertragungssysteme. Teil 1: Stationaerer Betriebszustand.
		Heidelberg: Hueting, 1983, Seite 51
		:param node_name_i:
		:param node_name_j:
		:return:
		"""
		
		# Summenadmittanz an Knoten i und entspricht einem Element der Knotenadmittanzmatrix (KAM)
		sum_admittance = Admittance(g=0, b=0)
		
		# Ist Diagonalelement ?
		is_diag_elem = node_name_i == node_name_j
		
		for bus_connecter in self.__bus_connecter_list:
			
			# pruefen ob das Objekt eine Leitung ist
			is_line = isinstance(bus_connecter, GridLine)
			
			if is_line:
				# echte Kopien der Längs- und Queradmittanz erzeugen
				bus_connecter_admittance = copy.deepcopy(bus_connecter.get_admittance()) if bus_connecter else 0
				bus_connecter_transverse_admittance = copy.deepcopy(
					bus_connecter.get_transverse_admittance_on_node()) if bus_connecter else 0
			
			else:
				# echte Kopie der Kurzschlussimpedanz des Transformators erstellen
				bus_connecter_admittance = copy.deepcopy(bus_connecter.get_sc_admittance()) if bus_connecter else 0
				bus_connecter_transverse_admittance = None
			# SPÄTER DIE SHUNT IMPEDANZ HINZUFUEGEN
			# bus_connecter_transverse_admittance = copy.deepcopy(
			# 	bus_connecter.get_transverse_admittance_on_node()) if bus_connecter else 0
			
			# pruefen ob Leitung beide Knoten verbindet
			is_element_connecting_i_j = bus_connecter.get_node_name_i() == node_name_i and \
			                            bus_connecter.get_node_name_j() == node_name_j or \
			                            bus_connecter.get_node_name_i() == node_name_j and \
			                            bus_connecter.get_node_name_j() == node_name_i
			
			# Prüfen ob Diagonalelement
			if is_diag_elem:
				# Addiere Längsadmittanz von Gridline zur Summenadmittanz
				sum_admittance += bus_connecter_admittance
				# Prüfen ob Queradmittanz in Gridline vorhanden
				if bus_connecter_transverse_admittance:
					# Addiere Knoten-Queradmittanz von Gridline zur Summenadmittanz
					sum_admittance += bus_connecter_transverse_admittance
			else:
				if is_element_connecting_i_j:
					# Addiere Längsadmittanz von Gridline zur Summenadmittanz
					sum_admittance += bus_connecter_admittance
		
		return sum_admittance if is_diag_elem else sum_admittance * -1
	
	# Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
	def calc_matrix(self, grid_node_list):
		
		# quadratische Matrixdimension: nxn
		number_of_grid_nodes = len(grid_node_list)
		
		# Erstellung eines nxn-dimensionalen Numpy-Arrays
		self.matrix = np.ndarray(shape=(number_of_grid_nodes, number_of_grid_nodes), dtype=object)
		
		# urspruengliche, ungefilterte Liste kopieren
		bus_connecter_list = copy.deepcopy(self.__bus_connecter_list)
		
		for row, grid_node in enumerate(grid_node_list):
			
			# Setzen der gefilterten Leitungsliste
			bus_connecter_list_with_node_name = [bus_connecter for bus_connecter in bus_connecter_list if
			                                     bus_connecter.get_node_name_i() == grid_node.name or
			                                     bus_connecter.get_node_name_j() == grid_node.name]
			
			self.__bus_connecter_list = copy.deepcopy(bus_connecter_list_with_node_name)
			
			for column in range(row, number_of_grid_nodes):
				gridnode_name_j = grid_node_list[column].name
				
				self.matrix[row][column] = self.matrix[column][row] = self.__get_sum_of_grid_lines_on_node(
					grid_node.name, gridnode_name_j)
	
	# Methode ermoeglicht das manuelle setzen einzelner Admittanz elemente
	def set_element(self, row, column, admittance):
		self.matrix[row][column] = admittance
		if row != column:
			self.matrix[column][row] = self.matrix[row][column]
