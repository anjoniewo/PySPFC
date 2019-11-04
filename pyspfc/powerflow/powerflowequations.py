import copy

"""
	source:  E. Handschin, "Elektrische Energieübertragunssysteme",
			 Teil 1: Stationärer Betriebszustand
	chapter: Lastflussberechnung - Newton-Raphson-Verfahren
	page:  80

	Fuer Referenz- (Slack) und Lastknoten (P-Q) gelten folgende Gleichungen:
	Summe ueber alle mit dem Knoten verbundenen Knoten ->

	Si = Pi + jQi
	Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
	Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

	voltage regulated grid nodes (P-U):

	Ui^2 = Ei^2 + Fi^2

	definition:

	Ui = Ei + jFi
	Ei = Re{Ui}
	Fi = Im{Ui}
	Yi = Gi + jBi
	Gi = Re{Yi}
	Bi = Im{Yi}
	"""


class LoadFlowEquations:
	def __init__(self, grid_node_list, bus_admittance_matrix):
		
		self.__grid_node_list = copy.deepcopy(grid_node_list)
		
		self.number_of_nodes = len(grid_node_list)
		
		self.__bus_admittance_matrix = bus_admittance_matrix
	
	def calculate_active_power_at_node(self, Fk_Ek_vector, grid_node_index):
		"""
		method calculates the active power at a grid node which is defined by Pi = Pg - Pl
		with Pg = generated active power and Pl = active power consumption
		:param Fk_Ek_vector:
		:param grid_node_index:
		:return:
		"""
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
	
	# Scheinleistung ueber Leitung von Knoten i nach Knoten j
	
	def calculate_s_from_node_i_to_node_j(self, grid_line, Fk_Ek_vector, grid_node_index_i, grid_node_index_j):
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index_i]
		Fi = Fk_Ek_vector[grid_node_index_i]
		Ej = Fk_Ek_vector[self.number_of_nodes + grid_node_index_j]
		Fj = Fk_Ek_vector[grid_node_index_j]
		Ui = Ei + Fi * 1j
		Uj = Ej + Fj * 1j
		
		# Laengsadmittanz zwischen den Knoten
		Yij = grid_line.get_admittance()
		if Yij.get_real_part() is not None and Yij.get_imaginary_part() is not None:
			Yij = Yij.get_real_part() + Yij.get_imaginary_part() * 1j
		else:
			Yij = 0
		
		# Queradmittanz der Leitung
		Y0i = grid_line.get_transverse_admittance_on_node()
		if Y0i.get_real_part() is not None and Y0i.get_imaginary_part() is not None:
			Y0i = Y0i.get_real_part() + Y0i.get_imaginary_part() * 1j
		else:
			Y0i = 0
		
		# komplexe Scheinleistung und komplexen Strom ueber Leitung berechnen
		Sij = Ui.conjugate() * (Ui - Uj) * Yij + (Ui.__abs__() ** 2) * Y0i
		Iij = Sij.conjugate() / Ui.conjugate()
		
		return Sij, Iij
	
	# Scheinleistung ueber Leitung von Knoten j nach Knoten i
	
	def calculate_s_from_node_j_to_node_i(self, grid_line, Fk_Ek_vector, grid_node_index_i, grid_node_index_j):
		Ei = Fk_Ek_vector[self.number_of_nodes + grid_node_index_i]
		Fi = Fk_Ek_vector[grid_node_index_i]
		Ej = Fk_Ek_vector[self.number_of_nodes + grid_node_index_j]
		Fj = Fk_Ek_vector[grid_node_index_j]
		Ui = Ei + Fi * 1j
		Uj = Ej + Fj * 1j
		
		# Laengsadmittanz zwischen den Knoten
		Yij = grid_line.get_admittance()
		if Yij.get_real_part() is not None and Yij.get_imaginary_part() is not None:
			Yij = Yij.get_real_part() + Yij.get_imaginary_part() * 1j
		else:
			Yij = 0
		
		# Queradmittanz der Leitung
		Y0i = grid_line.get_transverse_admittance_on_node()
		if Y0i.get_real_part() is not None and Y0i.get_imaginary_part() is not None:
			Y0i = Y0i.get_real_part() + Y0i.get_imaginary_part() * 1j
		else:
			Y0i = 0
		
		# komplexe Scheinleistung und komplexen Strom ueber Leitung berechnen
		Sji = Uj.conjugate() * (Uj - Ui) * Yij + (Uj.__abs__() ** 2) * Y0i
		Iji = Sji.conjugate() / Uj.conjugate()
		
		return Sji, Iji
	
	# Scheinleistung ueber Leitung von Knoten j nach Knoten i
	
	def calculate_s_over_transformer(self, transformer_name, Fk_Ek_vector, grid_node_index_i, grid_node_index_j):
		1
