import numpy as np

from .loadflowequations import *


def do_loadflow(grid):
    jacobi_matrix = grid.jacobi_matrix

    Fk_Ek_vector = jacobi_matrix.Fk_Ek_vector
    sub_Fk_Ek_vector = jacobi_matrix.sub_Fk_Ek_vector

    p_q_v_vector, indeces_and_node_types, number_of_voltage_nodes = create_initial_p_q_v_vector(jacobi_matrix,
                                                                                                grid.get_grid_node_list())

    number_of_nodes_without_slack = len(grid.get_grid_node_list()) - 1

    loadflowequations = LoadFlowEquations(grid.get_grid_node_list(), grid.get_bus_admittance_matrix())

    Fk_Ek_vector = do_iterations(jacobi_matrix, loadflowequations, indeces_and_node_types,
                                 number_of_nodes_without_slack,
                                 number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector)

    # calculate_p_q_v_vector(loadflowequations, indeces_and_node_types, )


def do_iterations(jacobian_matrix, loadflowequations, indeces_and_node_types, number_of_nodes_without_slack,
                  number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector):
    inverse_sub_jacobian = np.linalg.inv(jacobian_matrix.create_sub_jacobian_Jk(jacobian_matrix.J))

    for i in range(0, 2):
        Fk_Ek_vector = do_iteration(inverse_sub_jacobian, loadflowequations, indeces_and_node_types,
                                    number_of_nodes_without_slack,
                                    number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector)

        new_jacobian = jacobian_matrix.create_jacobian(Fk_Ek_vector)
        new_sub_jacobian = jacobian_matrix.create_sub_jacobian_Jk(new_jacobian)
        inverse_sub_jacobian = np.linalg.inv(new_sub_jacobian)

    return Fk_Ek_vector


def do_iteration(inverse_sub_jacobian, loadflowequations, indeces_and_node_types, number_of_nodes_without_slack,
                 number_of_voltage_nodes, Fk_Ek_vector, sub_Fk_Ek_vector, p_q_v_vector):
    p_q_v_iteration_vector = calculate_p_q_v_vector(loadflowequations, indeces_and_node_types,
                                                    number_of_nodes_without_slack, number_of_voltage_nodes,
                                                    Fk_Ek_vector)

    delta_p_q_v_vector = p_q_v_vector - p_q_v_iteration_vector

    Fk_Ek_iteration_vector = inverse_sub_jacobian.dot(delta_p_q_v_vector) + sub_Fk_Ek_vector

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


def create_initial_p_q_v_vector(jacobian_matrix, grid_node_list):
    number_of_nodes = len(grid_node_list)
    number_of_voltage_nodes = len(jacobian_matrix.get_indices_of_voltage_nodes())

    # Dimension des geküzten p_q_v_Vektors 2 * (n - 1), mit n = Anzahl aller Knoten
    p_q_v_vector_shape = 2 * (number_of_nodes - 1)
    p_q_v_vector = np.ndarray(shape=(p_q_v_vector_shape), dtype=float)

    index_in_vector = 0
    # 2(n - 1) - n_g
    voltage_node_offset = 2 * (number_of_nodes - 1) - number_of_voltage_nodes
    load_node_offset = number_of_nodes - number_of_voltage_nodes - 1

    indeces_and_node_types = np.ndarray(shape=(p_q_v_vector_shape), dtype=object)

    for index, grid_node in enumerate(grid_node_list):
        grid_node_number = grid_node.get_type_number()
        grid_node_type = grid_node.grid_node_types_index[grid_node_number]

        is_voltage_node = grid_node_number == grid_node.get_grid_node_type_index_of("voltage")
        is_load_node = grid_node_number == grid_node.get_grid_node_type_index_of("load")

        index_and_node_type = ()

        if is_voltage_node:
            # Netto-Wirkleistung eintragen
            active_power_index = index_in_vector
            p_q_v_vector[
                active_power_index] = grid_node.get_active_injection_power() - grid_node.get_active_load_power()

            # Spannungsquadrat eintragen
            voltage_index = index_in_vector + voltage_node_offset
            p_q_v_vector[voltage_index] = grid_node.get_node_voltage_magnitude() ** 2

            index_and_node_type = (index, grid_node_type)

            indeces_and_node_types[active_power_index] = index_and_node_type
            indeces_and_node_types[voltage_index] = index_and_node_type

            index_in_vector += 1

        elif is_load_node:
            active_power_index = index_in_vector
            p_q_v_vector[active_power_index] = grid_node.get_active_load_power()

            reactive_power_index = index_in_vector + load_node_offset
            p_q_v_vector[reactive_power_index] = grid_node.get_reactive_load_power()

            index_and_node_type = (index, grid_node_type)

            indeces_and_node_types[active_power_index] = index_and_node_type
            indeces_and_node_types[reactive_power_index] = index_and_node_type

            index_in_vector += 1

    return p_q_v_vector, indeces_and_node_types, number_of_voltage_nodes


def calculate_p_q_v_vector(loadflowequations, indices_and_node_types, number_of_nodes_without_slack,
                           number_of_voltage_nodes,
                           Fk_Ek_vector):
    p_q_v_iteration_vector = np.ndarray(shape=(2 * number_of_nodes_without_slack), dtype=float)

    # alle Wirkleistungen berechnen
    for index in range(0, number_of_nodes_without_slack):
        index_and_node_type = indices_and_node_types[index]
        grid_node_index = index_and_node_type[0]

        p_q_v_iteration_vector[index] = loadflowequations.calculate_active_power(Fk_Ek_vector, grid_node_index)

    for index in range(number_of_nodes_without_slack, 2 * number_of_nodes_without_slack):
        index_and_node_type = indices_and_node_types[index]
        grid_node_index = index_and_node_type[0]
        grid_node_type = index_and_node_type[1]

        if grid_node_type == "voltage":
            p_q_v_iteration_vector[index] = loadflowequations.calculate_node_voltage(Fk_Ek_vector, grid_node_index,
                                                                                     number_of_voltage_nodes)
        else:
            p_q_v_iteration_vector[index] = loadflowequations.calculate_reactive_power(Fk_Ek_vector, grid_node_index)

    return p_q_v_iteration_vector
