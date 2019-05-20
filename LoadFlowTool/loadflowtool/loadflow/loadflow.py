import numpy as np


def do_loadflow(grid):
	jacobi_matrix = grid.jacobi_matrix
	inverse_Jk = np.linalg.inv(jacobi_matrix.Jk)
	
	P_Q_V_vector = create_P_Q_V_vector(jacobi_matrix, grid.get_grid_node_list())


# Fk_Ek_vector


def create_P_Q_V_vector(jacobian_matrix, grid_node_list):
	voltage_node_indices = jacobian_matrix.get_indices_of_voltage_nodes()
	
	P_Q_V_vector_shape = (len(grid_node_list) * 2) + len(voltage_node_indices) + 1
	P_Q_V_vector = np.ndarray(shape=(P_Q_V_vector_shape), dtype=float)
	
	voltage_node_index = 0
	
	for index, grid_node in enumerate(grid_node_list):
		is_voltage_node = grid_node.get_type_number() == grid_node.get_grid_node_type_index_of("voltage")
		is_slack_node = grid_node.get_type_number() == grid_node.get_grid_node_type_index_of("slack")
		if is_voltage_node:
			P_Q_V_vector[voltage_node_index + (len(grid_node_list) * 2)] = grid_node.get_node_voltage_magnitude() ** 2
			voltage_node_index += 1
		elif is_slack_node:
			P_Q_V_vector[index] = None
			P_Q_V_vector[index + len(grid_node_list)] = None
			P_Q_V_vector[voltage_node_index + len(grid_node_list) * 2] = grid_node.get_node_voltage_magnitude() ** 2
			voltage_node_index += 1
		else:
			P_Q_V_vector[index] = grid_node.get_active_load_power
			P_Q_V_vector[index + len(grid_node_list)] = grid_node.get_reactive_load_power
	
	return P_Q_V_vector
