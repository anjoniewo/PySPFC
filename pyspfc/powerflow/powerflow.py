import numpy as np

from pyspfc.gridelements.gridnode import GridNode
from pyspfc.powerflow.jacobianmatrix import JacobianMatrix
from pyspfc.utils.complexutils import get_polar
from .powerflowequations import *


class PowerFlow:
	
	def __init__(self, **kwargs):
		
		self.v_nom = kwargs['v_nom'] if 'v_nom' in kwargs else None
		self.s_nom = kwargs['s_nom'] if 's_nom' in kwargs else None
		
		# Liste der Leitungen
		self.grid_line_list = kwargs['gridlines'] if 'gridlines' in kwargs else None
		
		# Liste der Transformatoren
		self.transformers = kwargs['transformers'] if 'transformers' in kwargs else None
		
		# urspruengliche, eingelesene Knotenliste
		self.grid_node_list = kwargs['gridnodes'] if 'gridnodes' in kwargs else None
		
		# Knotenliste die sich waehrend der Iterationen aendern kann
		# Beispiel:
		# Aus Spannungsknoten wird Lastknoten wenn Ungleichung Qmin <= Q <= Qmax nicht erfuellt ist
		self.new_grid_node_list = copy.deepcopy(self.grid_node_list)
		
		# initiale Spannungsknotennamen speichern
		self.initial_generator_node_names_and_indices = self.get_generator_node_names_and_index(self.grid_node_list)
		
		self.bus_admittance_matrix = kwargs['bus_admittance_matrix'] if 'bus_admittance_matrix' in kwargs else None
		
		self.jacobian_matrix = kwargs['jacobimatrix'] if 'jacobimatrix' in kwargs else None
		
		self.powerflowequations = None
		
		self.sub_p_q_v_vector = None
		
		self.init_Fk_Ek_vector = self.jacobian_matrix.Fk_Ek_vector
		
		self.nodes_that_exceeded_q_limit = set()
		
		self.grid_node_results = dict()
		
		self.grid_line_results = dict()
		
		self.export_result_df = None
	
	# Lastflussberechnung
	def do_powerflow(self):
		"""
			Method performs non-linear power flow calculation with Newton-Raphson algorithm
			results of each loop will be saved in lists and finally exported to csv files
		:return:
		"""
		
		# initialer Spannungsvektor ohne Slack-Elemente
		sub_Fk_Ek_vector = self.jacobian_matrix.get_sub_Fk_Ek_vector(self.init_Fk_Ek_vector)
		
		p_q_v_info_vector = self.jacobian_matrix.p_q_v_info_vector
		sub_p_q_v_info_vector = self.jacobian_matrix.sub_p_q_v_info_vector
		
		number_of_nodes = len(self.grid_node_list)
		
		self.powerflowequations = LoadFlowEquations(self.grid_node_list, self.bus_admittance_matrix)
		
		self.sub_p_q_v_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, None, initial=True)
		
		Fk_Ek_vector, sub_Fk_Ek_vector, self.iterations = self.do_iterations(Fk_Ek_vector=self.init_Fk_Ek_vector,
		                                                                     sub_Fk_Ek_vector=sub_Fk_Ek_vector,
		                                                                     sub_p_q_v_info_vector=sub_p_q_v_info_vector)
		
		p_q_v_vector = self.calculate_p_q_v_vector(p_q_v_info_vector, Fk_Ek_vector, initial=False)
		
		return self.create_node_results(p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector,
		                                number_of_nodes), self.create_line_results(Fk_Ek_vector)
	
	# iterative Lastflussberechnung mit Newton-Raphson verfahren durchfuehren
	def do_iterations(self, Fk_Ek_vector, sub_Fk_Ek_vector, sub_p_q_v_info_vector):
		sub_jacobian_Jk = self.jacobian_matrix.Jk
		inverse_sub_jacobian = np.linalg.inv(sub_jacobian_Jk)
		
		reached_convergence_limit = False
		reached_max_iteration = False
		iteration = 0
		MAX_ITERATIONS = 20
		self.CONVERGENCE_ACCURACY = 1e-6
		
		while (not reached_convergence_limit) and (not reached_max_iteration):
			Fk_Ek_vector, delta_p_q_v_vector, sub_p_q_v_iteration_vector = self.do_iteration(
				inverse_sub_jacobian=inverse_sub_jacobian,
				Fk_Ek_vector=Fk_Ek_vector,
				sub_Fk_Ek_vector=sub_Fk_Ek_vector,
				sub_p_q_v_info_vector=sub_p_q_v_info_vector)
			
			# Blindleistungsgrenzen der Einspeiseknoten pruefen und bei Verletzung die new_grid_node_list anpassen
			self.new_grid_node_list = self.check_q_limits(Fk_Ek_vector)
			
			sub_Fk_Ek_vector = self.jacobian_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)
			
			new_jacobi = JacobianMatrix(gridnodes=self.new_grid_node_list,
			                            voltagenodes=self.get_voltage_nodes(self.new_grid_node_list),
			                            bus_admittance_matrix=self.bus_admittance_matrix, Fk_Ek_vector=Fk_Ek_vector)
			
			new_sub_jacobian = new_jacobi.Jk
			inverse_sub_jacobian = np.linalg.inv(new_sub_jacobian)
			
			iteration += 1
			reached_max_iteration = True if iteration >= MAX_ITERATIONS else False
			reached_convergence_limit = self.check_convergency(delta_p_q_v_vector)
		
		return Fk_Ek_vector, sub_Fk_Ek_vector, iteration
	
	# Berechnungen der Teilvektoren einer Iteration durchfuehren
	def do_iteration(self, inverse_sub_jacobian, Fk_Ek_vector, sub_Fk_Ek_vector, sub_p_q_v_info_vector):
		
		sub_p_q_v_iteration_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, Fk_Ek_vector,
		                                                         initial=False)
		
		delta_p_q_v_vector = self.sub_p_q_v_vector - sub_p_q_v_iteration_vector
		delta_sub_Fk_Ek_vector = np.matmul(inverse_sub_jacobian, delta_p_q_v_vector)
		sub_Fk_Ek_iteration_vector = sub_Fk_Ek_vector + delta_sub_Fk_Ek_vector
		
		number_of_nodes_without_slack = len(self.grid_node_list) - 1
		new_Fk_Ek_vector = self.create_new_Fk_Ek_vector(Fk_Ek_vector, sub_Fk_Ek_iteration_vector,
		                                                number_of_nodes_without_slack)
		
		return new_Fk_Ek_vector, delta_p_q_v_vector, sub_p_q_v_iteration_vector
	
	# Methode prueft ob die Blindleistungsgrenzen der Spannungsgeregelten Knoten in jeder Iteraion eingehalten werden.
	# Falls nicht, wird aus einem PU-Knoten ein PQ- respektive Lastknoten
	def check_q_limits(self, Fk_Ek_vector):
		for tup in self.initial_generator_node_names_and_indices:
			index = tup[0]
			grid_node_name = tup[1]
			grid_node = next(
				(grid_node for grid_node in self.new_grid_node_list if grid_node.name == grid_node_name), None)
			
			grid_node_type = grid_node.get_type_number()
			if grid_node_type == 3:
				q_value_of_generator_node = self.powerflowequations.calculate_reactive_power_at_node(Fk_Ek_vector,
				                                                                                     index)
				q_min = grid_node.get_q_min()
				q_max = grid_node.get_q_max()
				exceeded_q_limit = False if q_min <= q_value_of_generator_node <= q_max else True
				
				if exceeded_q_limit:
					q_load = q_max if q_value_of_generator_node > q_max else q_min
					new_load_node = GridNode(grid_node_name, typenumber=2, p_load=grid_node.get_p_load(), q_load=q_load,
					                         q_max=q_max, q_min=q_min)
					
					self.new_grid_node_list[index] = new_load_node
			
			elif grid_node_type == 2:
				q_value_of_generator_node = self.powerflowequations.calculate_reactive_power_at_node(Fk_Ek_vector,
				                                                                                     index)
				q_min = grid_node.get_q_min()
				q_max = grid_node.get_q_max()
				if q_min <= q_value_of_generator_node <= q_max:
					node_index_in_origin_list, origin_node = self.get_index_and_grid_node_from_list(grid_node.name,
					                                                                                self.grid_node_list)
					self.new_grid_node_list[node_index_in_origin_list] = origin_node
				
				elif q_value_of_generator_node < q_min:
					index, grid_node = self.get_index_and_grid_node_from_list(grid_node_name, self.new_grid_node_list)
					self.new_grid_node_list[index].set_q_load(q_min)
				
				elif q_value_of_generator_node > q_max:
					index, grid_node = self.get_index_and_grid_node_from_list(grid_node_name, self.new_grid_node_list)
					self.new_grid_node_list[index].set_q_load(q_max)
		
		return self.new_grid_node_list
	
	def check_convergency(self, delta_p_q_v_vector):
		return True if max(delta_p_q_v_vector) < self.CONVERGENCE_ACCURACY else False
	
	# Methode gibt den Index sowie den Knoten aus der uebergebenen Knotenliste zurueck
	def get_index_and_grid_node_from_list(self, grid_node_name, grid_node_list):
		for index, grid_node in enumerate(grid_node_list):
			if grid_node.name == grid_node_name:
				return index, grid_node
	
	# Methode gibt den Index eines Knotens aus der uebergebenen Knotenliste zurueck
	def get_index_of_node_from_grid_node_list(self, grid_node_name, grid_node_list):
		for index, grid_node in enumerate(grid_node_list):
			if grid_node.name == grid_node_name:
				return index
	
	def get_voltage_nodes(self, grid_node_list):
		voltage_nodes_and_index = list(())
		for index, grid_node in enumerate(grid_node_list):
			if grid_node.get_type_number() == 3:
				voltage_nodes_and_index.append((index, grid_node))
		
		return voltage_nodes_and_index
	
	def get_generator_node_names_and_index(self, grid_node_list):
		voltage_node_names = list(())
		for index, grid_node in enumerate(grid_node_list):
			if grid_node.get_type_number() == 3:
				voltage_node_names.append((index, grid_node.name))
		
		return voltage_node_names
	
	def get_q_value_and_index(self, grid_node_name, sub_p_q_v_info_vector, p_q_v_iteration_vector):
		for index, item in enumerate(sub_p_q_v_info_vector):
			node_name = item[0]
			type_of_value = item[3]
			if node_name == grid_node_name and type_of_value == "Q":
				return p_q_v_iteration_vector[index], index
	
	# Spannungsvektor [Im{U}, Re{U}] berechnen
	def create_new_Fk_Ek_vector(self, Fk_Ek_vector, sub_Fk_Ek_iteration_vector, number_of_nodes_without_slack):
		index_of_slack = self.jacobian_matrix.index_of_slack
		Fk_slack = Fk_Ek_vector[index_of_slack]
		Ek_slack = Fk_Ek_vector[index_of_slack + number_of_nodes_without_slack + 1]
		
		Fk_Ek_vector = np.insert(sub_Fk_Ek_iteration_vector, index_of_slack, Fk_slack, 0)
		Fk_Ek_vector = np.insert(Fk_Ek_vector, index_of_slack + number_of_nodes_without_slack + 1, Ek_slack, 0)
		
		return Fk_Ek_vector
	
	def calculate_p_q_v_vector(self, p_q_v_info_vector, Fk_Ek_vector, initial=False):
		p_q_v_vector = np.ndarray(shape=(len(p_q_v_info_vector)), dtype=float)
		
		if initial:
			for index, item in enumerate(p_q_v_info_vector):
				value = item[4]
				p_q_v_vector[index] = value
		else:
			for index, item in enumerate(p_q_v_info_vector):
				# item[0] = Knotenname
				# item[1] = Knotentyp
				# item[2] = Knotenindex
				# item[3] = Elektrische Groeße
				# item[4] = Wert der elektrischen Groeße
				grid_node_index = item[2]
				type_of_value = item[3]
				
				if type_of_value == "P":
					p_q_v_vector[index] = self.powerflowequations.calculate_active_power_at_node(Fk_Ek_vector,
					                                                                             grid_node_index)
				elif type_of_value == "Q":
					p_q_v_vector[index] = self.powerflowequations.calculate_reactive_power_at_node(Fk_Ek_vector,
					                                                                               grid_node_index)
				elif type_of_value == "U":
					p_q_v_vector[index] = self.powerflowequations.calculate_node_voltage_at_node(Fk_Ek_vector,
					                                                                             grid_node_index)
		
		return p_q_v_vector
	
	def create_node_results(self, p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector, number_of_nodes):
		"""
		creates bus value datastructures of the powerflow results
		"""
		for index, item in enumerate(p_q_v_info_vector):
			
			grid_node_name = item[0]
			grid_node = [grid_node for grid_node in self.grid_node_list if grid_node.name == grid_node_name][0]
			type_number = grid_node.get_type_number()
			
			# item[0] = Knotenname
			# item[1] = Knotentyp
			# item[2] = Knotenindex
			# item[3] = Elektrische Groeße ("P", "Q" oder "U")
			# item[4] = Wert der elektrischen Groeße
			
			value = p_q_v_vector[index]
			if item[4] is None:
				item[4] = value
			
			# Dictionary anlegen wenn Key nicht vorhanden
			if not (grid_node_name in self.grid_node_results):
				self.grid_node_results[grid_node_name] = {}
				self.grid_node_results[grid_node_name]["Nodetyp"] = item[1]
			
			if grid_node.types_index[type_number] == "slack":
				if item[3] == "P":
					p_gross = item[4]
					p_load = grid_node.get_p_load()
					
					self.grid_node_results[grid_node_name]["p_load"] = p_load
					self.grid_node_results[grid_node_name]["p_gen"] = p_gross + p_load
					self.grid_node_results[grid_node_name]["p"] = p_gross
				
				elif item[3] == "Q":
					q_gross = item[4]
					
					q_load = grid_node.get_q_load()
					self.grid_node_results[grid_node_name]["q_load"] = q_load
					self.grid_node_results[grid_node_name]["q_gen"] = q_gross + q_load
					self.grid_node_results[grid_node_name]["q"] = q_gross
				
				elif item[3] == "U":
					self.grid_node_results[grid_node_name]["v_magnitude"] = grid_node.get_node_voltage_magnitude()
					self.grid_node_results[grid_node_name]["v_angle"] = grid_node.get_node_voltage_angle_in_rad()
			
			elif grid_node.types_index[type_number] == "PQ":
				if item[3] == "P":
					p_load = grid_node.get_p_load()
					self.grid_node_results[grid_node_name]["p_load"] = p_load
					self.grid_node_results[grid_node_name]["p_gen"] = 0
					self.grid_node_results[grid_node_name]["p"] = - p_load
				
				elif item[3] == "Q":
					q_load = grid_node.get_q_load()
					self.grid_node_results[grid_node_name]["q_load"] = q_load
					self.grid_node_results[grid_node_name]["q_gen"] = 0
					self.grid_node_results[grid_node_name]["q"] = - q_load
				
				elif item[3] == "U":
					u_result = get_polar(real=Fk_Ek_vector[item[2] + number_of_nodes], imaginary=Fk_Ek_vector[item[2]])
					self.grid_node_results[grid_node_name]["v_magnitude"] = u_result["magnitude"]
					self.grid_node_results[grid_node_name]["v_angle"] = u_result["angleGrad"]
			
			elif grid_node.types_index[type_number] == "PV":
				if item[3] == "P":
					p_load = grid_node.get_p_load()
					p_gen = grid_node.get_p_gen()
					self.grid_node_results[grid_node_name]["p_load"] = p_load
					self.grid_node_results[grid_node_name]["p_gen"] = p_gen
					self.grid_node_results[grid_node_name]["p"] = p_load + p_gen
				
				elif item[3] == "Q":
					q_gross = item[4]
					
					q_load = grid_node.get_q_load()
					q_gen = q_gross - q_load
					self.grid_node_results[grid_node_name]["q_load"] = q_load
					self.grid_node_results[grid_node_name]["q_gen"] = q_gen
					self.grid_node_results[grid_node_name]["q"] = q_gross
				
				elif item[3] == "U":
					u_result = get_polar(real=Fk_Ek_vector[item[2] + number_of_nodes], imaginary=Fk_Ek_vector[item[2]])
					self.grid_node_results[grid_node_name]["v_magnitude"] = u_result["magnitude"]
					self.grid_node_results[grid_node_name]["v_angle"] = u_result["angleGrad"]
		
		return self.grid_node_results
	
	def create_line_results(self, Fk_Ek_vector):
		"""
		creates line value datastructures of the powerflow results
		"""
		for grid_line in self.grid_line_list:
			grid_line_name = grid_line.name
			
			grid_node_name_i = grid_line.get_node_name_i()
			grid_node_name_j = grid_line.get_node_name_j()
			grid_node_index_i = self.get_index_of_node_from_grid_node_list(grid_node_name_i, self.grid_node_list)
			grid_node_index_j = self.get_index_of_node_from_grid_node_list(grid_node_name_j, self.grid_node_list)
			
			s_from_node_i_to_node_j, current_from_node_i_to_node_j = self.powerflowequations.calculate_s_from_node_i_to_node_j(
				grid_line, Fk_Ek_vector,
				grid_node_index_i,
				grid_node_index_j)
			
			s_from_node_j_to_node_i, current_from_node_j_to_node_i = self.powerflowequations.calculate_s_from_node_j_to_node_i(
				grid_line, Fk_Ek_vector,
				grid_node_index_i,
				grid_node_index_j)
			
			s_loss = s_from_node_i_to_node_j + s_from_node_j_to_node_i
			
			if not (grid_line_name in self.grid_node_results):
				self.grid_line_results[grid_line_name] = {}
				self.grid_line_results[grid_line_name]['bus_i'] = grid_node_name_i
				self.grid_line_results[grid_line_name]['bus_j'] = grid_node_name_j
			
			self.grid_line_results[grid_line_name]["s_from_i_to_j"] = round(float(np.absolute(s_from_node_i_to_node_j)),
			                                                                6)
			self.grid_line_results[grid_line_name]["p_from_i_to_j"] = round(float(s_from_node_i_to_node_j.real), 6)
			self.grid_line_results[grid_line_name]["q_from_i_to_j"] = round(float(s_from_node_i_to_node_j.imag), 6)
			self.grid_line_results[grid_line_name]["s_from_j_to_i"] = round(float(np.absolute(s_from_node_j_to_node_i)),
			                                                                6)
			self.grid_line_results[grid_line_name]["p_from_j_to_i"] = round(float(s_from_node_j_to_node_i.real), 6)
			self.grid_line_results[grid_line_name]["q_from_j_to_i"] = round(float(s_from_node_j_to_node_i.imag), 6)
			self.grid_line_results[grid_line_name]["p_loss"] = round(float(s_loss.real), 6)
			self.grid_line_results[grid_line_name]["q_loss"] = round(float(s_loss.imag), 6)
			self.grid_line_results[grid_line_name]["current_from_i_to_j"] = round(
				float(np.absolute(current_from_node_i_to_node_j)),
				6)
			self.grid_line_results[grid_line_name]["current_from_j_to_i"] = round(
				float(np.absolute(current_from_node_j_to_node_i)),
				6)
		
		return self.grid_line_results
	
	def __str__(self):
		result = str("\n")
		for i in range(105):
			result += str("-")
		result += str("\n")
		result += str("|")
		result += str("{:^10}".format("Knoten"))
		result += str("|")
		result += str("{:^30}".format("Einspeisung"))
		result += str("|")
		result += str("{:^30}".format("Last"))
		result += str("|")
		result += str("{:^30}".format("Spannung"))
		result += str("|\n")
		result += str("|")
		result += str("{:^10}".format("Name"))
		result += str("|")
		result += str("{:^15}".format("P_G"))
		result += str("{:^15}".format("Q_G"))
		result += str("|")
		result += str("{:^15}".format("P_L"))
		result += str("{:^15}".format("Q_L"))
		result += str("|")
		result += str("{:^15}".format("U_mag"))
		result += str("{:^15}".format("θ"))
		result += str("|\n")
		result += str("-") * 105
		result += str("\n")
		
		for key in self.grid_node_results:
			grid_node_name = key
			p_gen = self.grid_node_results[key]["P_gen"]
			q_gen = self.grid_node_results[key]["Q_gen"]
			p_load = self.grid_node_results[key]["P_load"]
			q_load = self.grid_node_results[key]["Q_load"]
			u_mag = self.grid_node_results[key]["U_magnitude"]
			theta = self.grid_node_results[key]["U_angle"]
			
			result += str("|")
			result += str("{:^10}".format(str(grid_node_name)))
			result += str("|")
			result += str("{:^15}".format(str(round(float(p_gen * self.s_nom), 3))))
			result += str("{:^15}".format(str(round(float(q_gen * self.s_nom), 3))))
			result += str("|")
			result += str("{:^15}".format(str(round(float(p_load * self.s_nom), 3))))
			result += str("{:^15}".format(str(round(float(q_load * self.s_nom), 3))))
			result += str("|")
			result += str("{:^15}".format(str(round(float(u_mag * self.v_nom), 3))))
			result += str("{:^15}".format(str(round(float(theta), 3)) + str("°")))
			result += str("|\n")
		
		result += str("-") * 105
		
		result += str("\n\n")
		
		result += str(
			"Die Konvergenzgrenze von Δx = " + str(self.CONVERGENCE_ACCURACY) + " wurde nach " + str(
				self.iterations) + " Iterationen erreicht.")
		return result
