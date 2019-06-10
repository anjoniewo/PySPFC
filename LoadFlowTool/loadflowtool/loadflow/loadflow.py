import numpy as np

from .loadflowequations import *


def do_loadflow(grid):
    jacobi_matrix = grid.jacobi_matrix

    Fk_Ek_vector = jacobi_matrix.Fk_Ek_vector
    sub_Fk_Ek_vector = jacobi_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)

    p_q_v_info_vector = jacobi_matrix.p_q_v_info_vector
    sub_p_q_v_info_vector = jacobi_matrix.sub_p_q_v_info_vector

    number_of_nodes_without_slack = len(grid.get_grid_node_list()) - 1

    # LÖSCHEN
    # number_of_voltage_nodes = jacobi_matrix.get_number_of_voltage_nodes()
    # LÖSCHEN

    index_of_slack = jacobi_matrix.index_of_slack

    loadflowequations = LoadFlowEquations(grid.get_grid_node_list(), grid.get_bus_admittance_matrix())

    sub_p_q_v_vector = calculate_p_q_v_vector(loadflowequations, sub_p_q_v_info_vector, Fk_Ek_vector, initial=True)

    Fk_Ek_vector, sub_Fk_Ek_vector = do_iterations(jacobian_matrix=jacobi_matrix, loadflowequations=loadflowequations,
                                                   number_of_nodes_without_slack=number_of_nodes_without_slack,
                                                   Fk_Ek_vector=Fk_Ek_vector, sub_Fk_Ek_vector=sub_Fk_Ek_vector,
                                                   sub_p_q_v_info_vector=sub_p_q_v_info_vector,
                                                   sub_p_q_v_vector=sub_p_q_v_vector, index_of_slack=index_of_slack)

    p_q_v_vector = calculate_p_q_v_vector(loadflowequations, p_q_v_info_vector, Fk_Ek_vector, initial=False)

    loadflow_result = create_result_info_vector(p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector)

    return loadflow_result


def do_iterations(jacobian_matrix, loadflowequations, number_of_nodes_without_slack, Fk_Ek_vector, sub_Fk_Ek_vector,
                  sub_p_q_v_info_vector, sub_p_q_v_vector, index_of_slack):
    sub_jacobian_Jk = jacobian_matrix.create_sub_jacobian_Jk(jacobian_matrix.J)
    inverse_sub_jacobian = np.linalg.inv(sub_jacobian_Jk)

    for i in range(0, 50):
        Fk_Ek_vector = do_iteration(inverse_sub_jacobian, loadflowequations, number_of_nodes_without_slack,
                                    Fk_Ek_vector, sub_Fk_Ek_vector, sub_p_q_v_info_vector, sub_p_q_v_vector,
                                    index_of_slack)

        sub_Fk_Ek_vector = jacobian_matrix.get_sub_Fk_Ek_vector(Fk_Ek_vector)

        new_jacobian = jacobian_matrix.create_jacobian(Fk_Ek_vector)
        new_sub_jacobian = jacobian_matrix.create_sub_jacobian_Jk(new_jacobian)
        inverse_sub_jacobian = np.linalg.inv(new_sub_jacobian)

    return Fk_Ek_vector, sub_Fk_Ek_vector


def do_iteration(inverse_sub_jacobian, loadflowequations, number_of_nodes_without_slack, Fk_Ek_vector, sub_Fk_Ek_vector,
                 sub_p_q_v_info_vector, sub_p_q_v_vector, index_of_slack):
    sub_p_q_v_iteration_vector = calculate_p_q_v_vector(loadflowequations, sub_p_q_v_info_vector, Fk_Ek_vector,
                                                        initial=False)

    delta_p_q_v_vector = sub_p_q_v_vector - sub_p_q_v_iteration_vector
    delta_sub_Fk_Ek_vector = inverse_sub_jacobian.dot(delta_p_q_v_vector)
    sub_Fk_Ek_iteration_vector = sub_Fk_Ek_vector + delta_sub_Fk_Ek_vector

    new_Fk_Ek_vector = calculate_new_Fk_Ek_vector(Fk_Ek_vector, sub_Fk_Ek_iteration_vector,
                                                  number_of_nodes_without_slack, index_of_slack)

    return new_Fk_Ek_vector


def calculate_new_Fk_Ek_vector(Fk_Ek_vector, sub_Fk_Ek_iteration_vector, number_of_nodes_without_slack, index_of_slack):
    Fk_slack = Fk_Ek_vector[index_of_slack]
    Ek_slack = Fk_Ek_vector[index_of_slack + number_of_nodes_without_slack + 1]

    Fk_Ek_vector = np.insert(sub_Fk_Ek_iteration_vector, index_of_slack, Fk_slack, 0)
    Fk_Ek_vector = np.insert(Fk_Ek_vector, index_of_slack + number_of_nodes_without_slack + 1, Ek_slack, 0)

    return Fk_Ek_vector


def calculate_p_q_v_vector(loadflowequations, p_q_v_info_vector, Fk_Ek_vector, initial=False):
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
                p_q_v_iteration_vector[index] = loadflowequations.calculate_active_power(Fk_Ek_vector, grid_node_index)

            elif type_of_value == "Q":
                p_q_v_iteration_vector[index] = loadflowequations.calculate_reactive_power(Fk_Ek_vector,
                                                                                           grid_node_index)
            elif type_of_value == "U":
                p_q_v_iteration_vector[index] = loadflowequations.calculate_node_voltage(Fk_Ek_vector, grid_node_index)

    return p_q_v_iteration_vector


def create_result_info_vector(p_q_v_info_vector, p_q_v_vector, Fk_Ek_vector):
    result_info_vector = {}

    for index, item in enumerate(p_q_v_info_vector):

        # item[0] = Knotenname
        # item[1] = Knotentyp
        # item[2] = Knotenindex
        # item[3] = Elektrische Groeße
        # item[4] = Wert der elektrischen Groeße

        value = p_q_v_vector[index]
        if item[4] is None:
            item[4] = value

        # Dictionary anlegen wenn Key(Knotenname) nicht vorhanden
        if not(str(item[0]) in result_info_vector):
            result_info_vector[str(item[0])] = {}

        if item[3] == "P":
            result_info_vector[str(item[0])]["P_load"] = item[4]
            result_info_vector[str(item[0])]["P_insection"] = item[4]

        if item[3] == "Q":
            result_info_vector[str(item[0])]["Q_load"] = item[4]
            result_info_vector[str(item[0])]["Q_insection"] = item[4]

        if item[3] == "U":
            result_info_vector[str(item[0])]["U_magnitude"] = item[4]
            result_info_vector[str(item[0])]["U_angle"] = Fk_Ek_vector

    return result_info_vector
