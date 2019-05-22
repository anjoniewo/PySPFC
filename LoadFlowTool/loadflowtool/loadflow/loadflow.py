import numpy as np

from .loadflowequations import *


def do_loadflow(grid):
	jacobi_matrix = grid.jacobi_matrix
	
	Fk_Ek_vector = jacobi_matrix.Fk_Ek_vector
	sub_Fk_Ek_vector = jacobi_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)
	
	p_q_v_info_vector = jacobi_matrix.p_q_v_info_vector
	
	number_of_nodes_without_slack = len(grid.get_grid_node_list()) - 1
	number_of_voltage_nodes = jacobi_matrix.get_number_of_voltage_nodes()
	
	loadflowequations = LoadFlowEquations(grid.get_grid_node_list(), grid.get_bus_admittance_matrix())
	
	p_q_v_vector = calculate_p_q_v_vector(loadflowequations, p_q_v_info_vector, Fk_Ek_vector, initial=True)
	
	Fk_Ek_vector, sub_Fk_Ek_vector = do_iterations(jacobi_matrix, loadflowequations,
	                                               number_of_nodes_without_slack,
	                                               number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector,
	                                               p_q_v_vector)
	
	p_q_v_vector = calculate_p_q_v_vector(loadflowequations, Fk_Ek_vector, initial=False)
	
	foo = ""


def do_iterations(jacobian_matrix, loadflowequations, number_of_nodes_without_slack, number_of_voltage_nodes,
                  Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector):
	
	sub_jacobian_Jk = jacobian_matrix.create_sub_jacobian_Jk(jacobian_matrix.J)
	inverse_sub_jacobian = np.linalg.inv(sub_jacobian_Jk)
	
	for i in range(0, 2):
		Fk_Ek_vector = do_iteration(inverse_sub_jacobian, loadflowequations, number_of_nodes_without_slack,
		                            number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector)
		
		sub_Fk_Ek_vector = jacobian_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)
		
		new_jacobian = jacobian_matrix.create_jacobian(Fk_Ek_vector)
		new_sub_jacobian = jacobian_matrix.create_sub_jacobian_Jk(new_jacobian)
		inverse_sub_jacobian = np.linalg.inv(new_sub_jacobian)
	
	return Fk_Ek_vector, sub_Fk_Ek_vector


def do_iteration(inverse_sub_jacobian, loadflowequations, indeces_and_node_types, number_of_nodes_without_slack,
                 number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector):
	p_q_v_iteration_vector = calculate_p_q_v_vector(loadflowequations, indeces_and_node_types, Fk_Ek_vector,
	                                                initial=False)
	
	delta_p_q_v_vector = p_q_v_vector - p_q_v_iteration_vector
	delta_sub_Fk_Ek_vector = inverse_sub_jacobian.dot(delta_p_q_v_vector)
	Fk_Ek_iteration_vector = sub_Fk_Ek_vector + delta_sub_Fk_Ek_vector
	
	new_Fk_Ek_vector = calculate_new_Fk_Ek_vector(Fk_Ek_vector, Fk_Ek_iteration_vector, indeces_and_node_types,
	                                              number_of_nodes_without_slack, number_of_voltage_nodes)
	
	return new_Fk_Ek_vector


def calculate_new_Fk_Ek_vector(Fk_Ek_vector, Fk_Ek_iteration_vector, indeces_and_node_types,
                               number_of_nodes_without_slack, number_of_voltage_nodes):
	for index, entry in enumerate(Fk_Ek_iteration_vector):
		index_and_node_type = indeces_and_node_types[index]
		original_index = index_and_node_type[0]
		
		if index < number_of_nodes_without_slack:
			Fk_Ek_vector[original_index] = entry
		else:
			grid_node_type = index_and_node_type[1]
			
			if grid_node_type == "load":
				Fk_Ek_vector[original_index + number_of_nodes_without_slack + 1] = entry
			else:
				Fk_Ek_vector[original_index + number_of_nodes_without_slack + 1 + number_of_voltage_nodes] = entry
	
	return Fk_Ek_vector

def calculate_p_q_v_vector(loadflowequations, p_q_v_info_vector, Fk_Ek_vector, initial=False):
	p_q_v_iteration_vector = np.ndarray(shape=(len(p_q_v_info_vector)), dtype=float)
	
	if initial:
		for index, item in enumerate(p_q_v_info_vector):
			value = item[3]
			p_q_v_iteration_vector[index] = value
	else:
		for index, item in enumerate(p_q_v_info_vector):
			# node_name_and_x_value[0] = Knotenname
			# node_name_and_x_value[1] = Knotentyp
			# node_name_and_x_value[2] = Knotenindex
			# node_name_and_x_value[3] = Elektrische Groeße
			# node_name_and_x_value[4] = Wert der elektrischen Groeße
			grid_node_index = item[2]
			type_of_value = item[4]
			
			if type_of_value == "P":
				p_q_v_iteration_vector[index] = loadflowequations.calculate_active_power(Fk_Ek_vector, grid_node_index)
			elif type_of_value == "Q":
				p_q_v_iteration_vector[index] = loadflowequations.calculate_reactive_power(Fk_Ek_vector,
				                                                                           grid_node_index)
			elif type_of_value == "U":
				p_q_v_iteration_vector[index] = loadflowequations.calculate_node_voltage(Fk_Ek_vector, grid_node_index)
	
	return p_q_v_iteration_vector
