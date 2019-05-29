import numpy as np

from LoadFlowTool.loadflowtool.loadflow.jacobianmatrix import JacobianMatrix
from .loadflowequations import *
from LoadFlowTool.loadflowtool.utils.complexutils import get_polar
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode


class LoadFlow:
	
	def __init__(self, grid):
		
		self.grid_node_list = grid.get_grid_node_list()
		
		self.new_grid_node_list = list()
		
		self.bus_admittance_matrix = grid.get_bus_admittance_matrix()
		
		self.jacobian_matrix = grid.jacobi_matrix
		
		self.loadflowequations = None
		
		self.nodes_that_exceeded_q_limit = list()
		
		self.loadflow_result = None
		
		# Lastflussberechnung durchfuehren
		self.do_loadflow(grid)
	
	# Lastflussberechnung
	def do_loadflow(self, grid):
		
		Fk_Ek_vector = self.jacobian_matrix.Fk_Ek_vector
		sub_Fk_Ek_vector = self.jacobian_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)
		
		p_q_v_info_vector = self.jacobian_matrix.p_q_v_info_vector
		sub_p_q_v_info_vector = self.jacobian_matrix.sub_p_q_v_info_vector
		
		number_of_nodes = len(self.grid_node_list)
		
		self.loadflowequations = LoadFlowEquations(grid.get_grid_node_list(), self.bus_admittance_matrix)
		
		sub_p_q_v_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, Fk_Ek_vector, initial=True)
		
		Fk_Ek_vector, sub_Fk_Ek_vector, self.iterations = self.do_iterations(Fk_Ek_vector=Fk_Ek_vector,
		                                                                     sub_Fk_Ek_vector=sub_Fk_Ek_vector,
		                                                                     sub_p_q_v_info_vector=sub_p_q_v_info_vector,
		                                                                     sub_p_q_v_vector=sub_p_q_v_vector)
		
		p_q_v_vector = self.calculate_p_q_v_vector(p_q_v_info_vector, Fk_Ek_vector, initial=False)
		
		self.loadflow_result = self.create_result_info_vector(p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector,
		                                                      number_of_nodes)
	
	# iterative Lastflussberechnung mit Newton-Raphson verfahren durchfuehren
	def do_iterations(self, Fk_Ek_vector, sub_Fk_Ek_vector,
	                  sub_p_q_v_info_vector, sub_p_q_v_vector):
		sub_jacobian_Jk = self.jacobian_matrix.Jk
		inverse_sub_jacobian = np.linalg.inv(sub_jacobian_Jk)
		
		reached_convergence_limit = False
		reached_max_iteration = False
		iteration = 0
		MAX_ITERATIONS = 50
		self.CONVERGENCE_ACCURACY = 1e-6
		sub_p_q_v_iteration_vector = np.zeros(len(sub_p_q_v_info_vector))
		
		while (not reached_convergence_limit) and (not reached_max_iteration):
			Fk_Ek_vector, delta_p_q_v_vector, sub_p_q_v_iteration_vector = self.do_iteration(
				inverse_sub_jacobian=inverse_sub_jacobian,
				Fk_Ek_vector=Fk_Ek_vector,
				sub_Fk_Ek_vector=sub_Fk_Ek_vector,
				sub_p_q_v_info_vector=sub_p_q_v_info_vector,
				sub_p_q_v_vector=sub_p_q_v_vector)
			
			checked_new_load_nodes = False
			if len(self.nodes_that_exceeded_q_limit) > 0:
				jacobian_with_changed_nodes = self.check_new_load_nodes_q_limit(sub_p_q_v_iteration_vector)
				sub_p_q_v_info_vector = jacobian_with_changed_nodes.sub_p_q_v_info_vector
				sub_p_q_v_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, Fk_Ek_vector,
				                                               initial=True)
				self.jacobian_matrix = jacobian_with_changed_nodes
				checked_new_load_nodes = True
			
			if not checked_new_load_nodes:
				self.new_grid_node_list = self.check_q_limits(sub_p_q_v_iteration_vector)
				if self.new_grid_node_list:
					jacobian_with_changed_nodes = JacobianMatrix(self.new_grid_node_list,
					                                             self.get_voltage_nodes(self.new_grid_node_list),
					                                             self.bus_admittance_matrix, Fk_Ek_vector)
					
					if jacobian_with_changed_nodes:
						sub_p_q_v_info_vector = jacobian_with_changed_nodes.sub_p_q_v_info_vector
						sub_p_q_v_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, Fk_Ek_vector,
						                                               initial=True)
						self.jacobian_matrix = jacobian_with_changed_nodes
			
			sub_Fk_Ek_vector = self.jacobian_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)
			
			new_jacobian_matrix = self.jacobian_matrix.create_jacobian(Fk_Ek_vector)
			new_sub_jacobian = self.jacobian_matrix.create_sub_jacobian_Jk(new_jacobian_matrix)
			inverse_sub_jacobian = np.linalg.inv(new_sub_jacobian)
			
			iteration += 1
			reached_max_iteration = True if iteration == MAX_ITERATIONS else False
			vector_norm = np.linalg.norm(delta_p_q_v_vector)
			reached_convergence_limit = True if vector_norm < self.CONVERGENCE_ACCURACY else False
		
		return Fk_Ek_vector, sub_Fk_Ek_vector, iteration
	
	# Berechnungen der Teilvektoren einer Iteration durchfuehren
	def do_iteration(self, inverse_sub_jacobian, Fk_Ek_vector, sub_Fk_Ek_vector, sub_p_q_v_vector,
	                 sub_p_q_v_info_vector):
		
		sub_p_q_v_iteration_vector = self.calculate_p_q_v_vector(sub_p_q_v_info_vector, Fk_Ek_vector,
		                                                         initial=False)
		
		delta_p_q_v_vector = sub_p_q_v_vector - sub_p_q_v_iteration_vector
		delta_sub_Fk_Ek_vector = inverse_sub_jacobian.dot(delta_p_q_v_vector)
		sub_Fk_Ek_iteration_vector = sub_Fk_Ek_vector + delta_sub_Fk_Ek_vector
		
		number_of_nodes_without_slack = len(self.grid_node_list) - 1
		new_Fk_Ek_vector = self.calculate_new_Fk_Ek_vector(Fk_Ek_vector, sub_Fk_Ek_iteration_vector,
		                                                   number_of_nodes_without_slack)
		
		return new_Fk_Ek_vector, delta_p_q_v_vector, sub_p_q_v_iteration_vector
	
	# Methode prueft ob die Blindleistungsgrenzen der Spannungsgeregelten Knoten in jeder Iteraion eingehalten werden.
	# Falls nicht, wird aus einem PU-Knoten ein PQ- respektive Lastknoten
	def check_q_limits(self, sub_p_q_v_iteration_vector):
		
		voltage_nodes_info_vector = [item for item in self.jacobian_matrix.p_q_v_info_vector if
		                             item[1] == "voltage" and item[3] == "Q"]
		exceeded_limit = False
		for index, item in enumerate(voltage_nodes_info_vector):
			grid_node_name = item[0]
			grid_node_type = item[1]
			type_of_value = item[3]
			
			q_value = sub_p_q_v_iteration_vector[index]
			voltage_node_index, p_u_node = self.get_index_and_grid_node_from_list(grid_node_name)
			q_min = p_u_node.get_q_min()
			q_max = p_u_node.get_q_max()
			exceeded_limit = False if q_min <= q_value <= q_max else True
			
			if exceeded_limit:
				self.nodes_that_exceeded_q_limit.append((self.grid_node_list[voltage_node_index], index))
				q_load = q_max if q_value > q_max else q_min
				node_parameters = [p_u_node.get_p_load(), q_load]
				new_load_node = GridNode(grid_node_name, 2, node_parameters)
				self.new_grid_node_list = copy.deepcopy(self.grid_node_list)
				self.new_grid_node_list[voltage_node_index] = new_load_node
		
		if exceeded_limit:
			return self.new_grid_node_list
		else:
			return False
	
	def get_index_and_grid_node_from_list(self, grid_node_name):
		for index, grid_node in enumerate(self.grid_node_list):
			if grid_node.get_name() == grid_node_name:
				return index, grid_node
	
	def get_voltage_nodes(self, grid_node_list):
		return [grid_node for grid_node in grid_node_list if grid_node.get_type_number() == 3]
	
	def check_new_load_nodes_q_limit(self, sub_p_q_v_iteration_vector):
		
		for grid_node, origin_index in self.nodes_that_exceeded_q_limit:
			grid_node_name = grid_node.get_name()
			# node_index, grid_node = self.get_index_and_grid_node_from_list(grid_node_name)
			q_min = grid_node.get_q_min()
			q_max = grid_node.get_q_max()
			q_value = sub_p_q_v_iteration_vector[origin_index]
			
			if q_min <= q_value <= q_max:
				self.nodes_that_exceeded_q_limit.remove((grid_node, origin_index))
				node_index_in_origin_list, origin_node = self.get_index_and_grid_node_from_list(grid_node.get_name())
				self.new_grid_node_list[node_index_in_origin_list] = origin_node
			elif q_value < q_min:
				foo = ""
			elif q_value > q_max:
				foo = ""
			
			return JacobianMatrix(self.new_grid_node_list, self.get_voltage_nodes(self.new_grid_node_list),
			                      self.bus_admittance_matrix)
	
	# Spannungsvektor [Im{U}, Re{U}] berechnen
	def calculate_new_Fk_Ek_vector(self, Fk_Ek_vector, sub_Fk_Ek_iteration_vector, number_of_nodes_without_slack):
		index_of_slack = self.jacobian_matrix.index_of_slack
		Fk_slack = Fk_Ek_vector[index_of_slack]
		Ek_slack = Fk_Ek_vector[index_of_slack + number_of_nodes_without_slack + 1]
		
		Fk_Ek_vector = np.insert(sub_Fk_Ek_iteration_vector, index_of_slack, Fk_slack, 0)
		Fk_Ek_vector = np.insert(Fk_Ek_vector, index_of_slack + number_of_nodes_without_slack + 1, Ek_slack, 0)
		
		return Fk_Ek_vector
	
	def calculate_p_q_v_vector(self, p_q_v_info_vector, Fk_Ek_vector, initial=False):
		p_q_v_iteration_vector = np.ndarray(shape=(len(p_q_v_info_vector)), dtype=float)
		
		if initial:
			for index, item in enumerate(p_q_v_info_vector):
				value = item[4]
				p_q_v_iteration_vector[index] = value
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
					p_q_v_iteration_vector[index] = self.loadflowequations.calculate_active_power(Fk_Ek_vector,
					                                                                              grid_node_index)
				
				elif type_of_value == "Q":
					p_q_v_iteration_vector[index] = self.loadflowequations.calculate_reactive_power(Fk_Ek_vector,
					                                                                                grid_node_index)
				elif type_of_value == "U":
					p_q_v_iteration_vector[index] = self.loadflowequations.calculate_node_voltage(Fk_Ek_vector,
					                                                                              grid_node_index)
		
		return p_q_v_iteration_vector
	
	def create_result_info_vector(self, p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector, number_of_nodes):
		result_info_vector = {}
		
		for index, item in enumerate(p_q_v_info_vector):
			
			grid_node_name = item[0]
			grid_node = [grid_node for grid_node in self.grid_node_list if grid_node.get_name() == grid_node_name][0]
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
			if not (str(item[0]) in result_info_vector):
				result_info_vector[str(item[0])] = {}
				result_info_vector[str(item[0])]["Nodetyp"] = item[1]
			
			if grid_node.types_index[type_number] == "slack":
				if item[3] == "P":
					p_gross = item[4]
					p_load = grid_node.get_p_load()
					
					result_info_vector[str(item[0])]["P_load"] = p_load
					result_info_vector[str(item[0])]["P_injection"] = p_gross + p_load
				
				elif item[3] == "Q":
					q_gross = item[4]
					
					q_load = grid_node.get_q_load()
					result_info_vector[str(item[0])]["Q_load"] = q_load
					result_info_vector[str(item[0])]["Q_injection"] = q_gross + q_load
				
				elif item[3] == "U":
					result_info_vector[str(item[0])]["U_magnitude"] = grid_node.get_node_voltage_magnitude()
					result_info_vector[str(item[0])]["U_angle"] = grid_node.get_node_voltage_angle_in_rad()
			
			elif grid_node.types_index[type_number] == "load":
				u_result = get_polar(real=Fk_Ek_vector[item[2] + number_of_nodes], imaginary=Fk_Ek_vector[item[2]])
				result_info_vector[str(item[0])]["U_magnitude"] = u_result["magnitude"]
				result_info_vector[str(item[0])]["U_angle"] = u_result["angleGrad"]
				
				if item[3] == "P":
					p_load = grid_node.get_p_load()
					result_info_vector[str(item[0])]["P_load"] = p_load
					result_info_vector[str(item[0])]["P_injection"] = 0
				
				elif item[3] == "Q":
					q_load = grid_node.get_q_load()
					result_info_vector[str(item[0])]["Q_load"] = q_load
					result_info_vector[str(item[0])]["Q_injection"] = 0
			
			elif grid_node.types_index[type_number] == "voltage":
				if item[3] == "P":
					p_load = grid_node.get_p_load()
					p_injection = grid_node.get_p_injection()
					result_info_vector[str(item[0])]["P_load"] = p_load
					result_info_vector[str(item[0])]["P_injection"] = p_injection
				
				elif item[3] == "Q":
					q_load = grid_node.get_q_load()
					q_injection = q_gross - q_load
					result_info_vector[str(item[0])]["Q_load"] = q_load
					result_info_vector[str(item[0])]["Q_injection"] = q_injection
				
				elif item[3] == "U":
					u_result = get_polar(real=Fk_Ek_vector[item[2] + number_of_nodes], imaginary=Fk_Ek_vector[item[2]])
					result_info_vector[str(item[0])]["U_magnitude"] = u_result["magnitude"]
					result_info_vector[str(item[0])]["U_angle"] = u_result["angleGrad"]
		
		return result_info_vector
	
	def __str__(self):
		result = str("\n")
		result += str(
			"Die angebenen Werte (in p.u.) beziehen sich auf die Bezugsgroeßen U_nom = 400 V und S_nom = 220 MVA\n\n")
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
		for i in range(105):
			result += str("-")
		result += str("\n")
		
		for key in self.loadflow_result:
			grid_node_name = key
			p_injection = self.loadflow_result[key]["P_injection"]
			q_injection = self.loadflow_result[key]["Q_injection"]
			p_load = self.loadflow_result[key]["P_load"]
			q_load = self.loadflow_result[key]["Q_load"]
			u_mag = self.loadflow_result[key]["U_magnitude"]
			theta = self.loadflow_result[key]["U_angle"]
			
			result += str("|")
			result += str("{:^10}".format(str(grid_node_name)))
			result += str("|")
			result += str("{:^15}".format(str(round(float(p_injection), 3))))
			result += str("{:^15}".format(str(round(float(q_injection), 3))))
			result += str("|")
			result += str("{:^15}".format(str(round(float(p_load), 3))))
			result += str("{:^15}".format(str(round(float(q_load), 3))))
			result += str("|")
			result += str("{:^15}".format(str(round(float(u_mag), 3))))
			result += str("{:^15}".format(str(round(float(theta), 3)) + str("°")))
			result += str("|\n")
		
		for i in range(105):
			result += str("-")
		
		result += str("\n\n")
		
		result += str(
			"Die Konvergenzgrenze von Δx = " + str(self.CONVERGENCE_ACCURACY) + " wurde nach " + str(
				self.iterations) + " Iterationen erreicht.")
		return result
