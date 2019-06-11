"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Lastflussberechnung - Newton-Raphson-Verfahren
Seiten:  80

Fuer Referenz- (Slack) und Lastknoten (P-Q) gelten folgende Gleichungen:
Summe ueber alle mit dem Knoten verbundenen Knoten ->

Si = Pi + jQi
Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

Fuer spannungsgeregelte Knoten (P-U) gilt:

Ui^2 = Ei^2 + Fi^2

Definitionen:

Ui = Ei + jFi
Ei = Re{Ui}
Fi = Im{Ui}
Yi = Gi + jBi
Gi = Re{Yi}
Bi = Im{Yi}

"""

import copy

import math


class LoadFlowEquations:
	
	def __init__(self, grid_node_list, bus_admittance_matrix):
		
		self.__grid_node_list = copy.deepcopy(grid_node_list)
		
		self.number_of_nodes = len(grid_node_list)
		
		self.__bus_admittance_matrix = bus_admittance_matrix
	
	# Lastflussgleichung - Wirkleistung an einem Knoten
	def calculate_active_power_at_node(self, Fk_Ek_vector, grid_node_index):
		
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		Pi = 0
		for j in range(self.number_of_nodes):
			Ej = Fk_Ek_vector[self.number_of_nodes + j]
			Fj = Fk_Ek_vector[j]
			Yij = self.__bus_admittance_matrix[grid_node_index][j]
			Gij = Yij.get_real_part()
			Bij = Yij.get_imaginary_part()
			
			Pi += (Ei * ((Ej * Gij) - (Fj * Bij))) + (Fi * ((Fj * Gij) + (Ej * Bij)))
		return Pi
	
	# Lastflussgleichung - Blindleistung an einem Knoten
	def calculate_reactive_power_at_node(self, Fk_Ek_vector, grid_node_index):
		
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		Qi = 0
		for j in range(self.number_of_nodes):
			Ej = Fk_Ek_vector[self.number_of_nodes + j]
			Fj = Fk_Ek_vector[j]
			Yij = self.__bus_admittance_matrix[grid_node_index][j]
			Gij = Yij.get_real_part()
			Bij = Yij.get_imaginary_part()
			
			Qi += (Fi * ((Ej * Gij) - (Fj * Bij))) - (Ei * ((Fj * Gij) + (Ej * Bij)))
		return Qi
	
	# Knotenspannung berechnen
	def calculate_node_voltage_at_node(self, Fk_Ek_vector, grid_node_index):
		
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		Ui_2 = (Ei ** 2) + (Fi ** 2)
		return Ui_2
	
	# Wirkleistungsfluss ueber eine Leitung
	def calculate_p_over_line(self, grid_line, Fk_Ek_vector, grid_node_index_i, grid_node_index_j):
		
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index_i]
		Fi = Fk_Ek_vector[grid_node_index_i]
		Ei2 = Ei ** 2
		Fi2 = Fi ** 2
		Ej = Fk_Ek_vector[self.number_of_nodes + grid_node_index_j]
		Fj = Fk_Ek_vector[grid_node_index_j]
		Ej2 = Ej ** 2
		Fj2 = Fj ** 2
		
		# Laengsadmittanz zwischen den Knoten
		Yij = grid_line.get_admittance()
		Gij = Yij.get_real_part()
		Bij = Yij.get_imaginary_part()
		
		# Queradmittanz der Leitung
		Y0i = grid_line.get_transverse_admittance_on_node()
		has_transverse_g = True if Y0i.get_real_part() is not None else False
		# Konduktanz der Queradmittanz
		G0i = Y0i.get_real_part() if has_transverse_g else 0
		
		Pij = Gij * (Ei2 + Fi2 - (Ei * Ej) - (Fi * Fj)) + Bij * ((Fi * Ej) - (Fj * Ei)) + G0i * (Ei2 + Fi2)
		
		return Pij
	
	# Blindleistungsfluss ueber eine Leitung
	def calculate_q_over_line(self, grid_line, Fk_Ek_vector, grid_node_index_i, grid_node_index_j):
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index_i]
		Fi = Fk_Ek_vector[grid_node_index_i]
		Ei2 = Ei ** 2
		Fi2 = Fi ** 2
		Ej = Fk_Ek_vector[self.number_of_nodes + grid_node_index_j]
		Fj = Fk_Ek_vector[grid_node_index_j]
		Ej2 = Ej ** 2
		Fj2 = Fj ** 2
		
		# Laengsadmittanz zwischen den Knoten
		Yij = grid_line.get_admittance()
		Gij = Yij.get_real_part()
		Bij = Yij.get_imaginary_part()
		
		# Queradmittanz der Leitung
		Y0i = grid_line.get_transverse_admittance_on_node()
		has_transverse_b = True if Y0i.get_imaginary_part() is not None else False
		# Konduktanz der Queradmittanz
		B0i = Y0i.get_real_part() if has_transverse_b else 0
		
		Qij = Bij * (Ei2 + Fi2 - (Ei * Ej) - (Fi * Fj)) + Gij * ((Fi * Ej) - (Fj * Ei)) + B0i * (Ei2 + Fi2)
		
		return Qij
	
	# komplexer Strom ueber eine Leitung
	def calculate_current_over_line(self, line_name):
		1
