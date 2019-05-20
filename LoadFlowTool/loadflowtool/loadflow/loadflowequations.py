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


class LoadFlowEquations:
	
	def __init__(self, grid_node_list, bus_admittance_matrix, Fk_Ek_vector):
		self.__grid_node_list = copy.deepcopy(grid_node_list)
		
		self.__active_load_equations = list()
		
		self.__reactive_load_equations = list()
	
	# Lastflussgleichung - Wirkleistung
	def calculate_active_power(self, bus_admittance_matrix, Fk_Ek_vector, grid_node_index):
		Ei = Fk_Ek_vector[len(self.__grid_node_list) + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		Pi = 0
		for j in range(0, len(self.__grid_node_list)):
			Ej = Fk_Ek_vector[len(self.__grid_node_list) + j]
			Fj = Fk_Ek_vector[j]
			Yij = bus_admittance_matrix[grid_node_index][j]
			Gij = Yij.get_real_part()
			Bij = Yij.get_imaginary_part()
			
			Pi += Ei * ((Ej * Gij) - (Fj * Bij)) + Fi * ((Fj * Gij) + (Ej * Bij))
		return Pi
	
	# Lastflussgleichung - Blindleistung
	def calculate_reactive_power(self, bus_admittance_matrix, Fk_Ek_vector, grid_node_index):
		Ei = Fk_Ek_vector[len(self.__grid_node_list) + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		Qi = 0
		for j in range(0, len(self.__grid_node_list)):
			Ej = Fk_Ek_vector[len(self.__grid_node_list) + j]
			Fj = Fk_Ek_vector[j]
			Yij = bus_admittance_matrix[grid_node_index][j]
			Gij = Yij.get_real_part()
			Bij = Yij.get_imaginary_part()
			
			Qi += Fi * ((Ej * Gij) - (Fj * Bij)) - Ei * ((Fj * Gij) + (Ej * Bij))
		return Qi
	
	# Knotenspannung berechnen
	def calculate_node_voltage(self, Fk_Ek_vector, grid_node_index):
		Ei = Fk_Ek_vector[len(self.__grid_node_list) + grid_node_index]
		Fi = Fk_Ek_vector[grid_node_index]
		return Ei ** 2 + Fi ** 2
