from simplepowerflow.powerflow.utils.complexutils import get_cartesian_from_euler
import numpy as np

"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Lastflussberechnung - Newton-Raphson-Verfahren
Seiten:  80

Aus der Jacobimatrix J werden die Gleichungen des Slackknotens gestrichen:

=> dim(J) = (m, m) -> dim(Jk) = (m-2, m-2)

Aufbau der Jacobimatrix J:
                             |                     |                    |     | ΔF1 |     |  ΔP1  |
                             |                     |                    |     |  .  |     |   .   |
                             |    Jk1 = δPi/δFj    |   Jk2 = δPi/δEj    |     |  .  |     |   .   |
                             |                     |                    |     |  .  |     |   .   |
                             |                     |                    |     |  .  |     |  ΔPn  |
                             |------------------------------------------|     |  .  |     |   .   |
			                 |                     |                    |     |  .  |     |  ΔQ1  |
			                 |                     |                    |     | ΔFn |     |   .   |
 [J] * {Fk_Ek} = {P,Q,U} =>  |   Jk3 = δQi/δFj     |    Jk4 = δQi/δEj   |  *  |-----|  =  |-------|
                             |                     |                    |     | ΔEn |     |   .   |
                             |                     |                    |     |  .  |     |  ΔQn  |
                             |---------------------|--------------------|     |  .  |     |   .   |
                             |                     |                    |     |  .  |     | ΔU1^2 |
                             |                     |                    |     |  .  |     |   .   |
                             |   Jk5 = δUi/δFj     |    Jk6 = δUi/δEj   |     |  .  |     |   .   |
                             |                     |                    |     |  .  |     |   .   |
                             |                     |                    |     | ΔEn |     | ΔUn^2 |
"""


class JacobianMatrix:

    def __init__(self, **kwargs):

        # Liste der Netzknoten
        self.__grid_node_list = kwargs['gridnodes'] if 'gridnodes' in kwargs else None

        # Anzahl an Netzknoten
        self.__number_of_nodes = len(self.__grid_node_list)

        # Liste der Spannungsknoten
        self.__list_of_voltage_nodes = kwargs['voltagenodes'] if 'voltagenodes' in kwargs else None

        # Anzahl der Spannungsknoten
        self.__number_of_voltage_nodes = len(self.__list_of_voltage_nodes)

        # Knotenadmittanzmatrix
        self.__bus_admittance_matrix = kwargs['bus_admittance_matrix'] if 'bus_admittance_matrix' in kwargs else None

        self.index_of_slack = next((index for index, grid_node in enumerate(self.__grid_node_list) if
                                    grid_node.get_type_number() == self.__grid_node_list[
                                        index].get_grid_node_type_index_of("slack")), None)

        self.Fk_Ek_vector = self.sub_Fk_Ek_vector = kwargs[
            'Fk_Ek_vector'] if 'Fk_Ek_vector' in kwargs else self.init_Fk_Ek_vector()

        self.p_q_v_info_vector = self.create_p_q_v_info_vector()

        # wird bei der Erstellung der SubJacobi Jk geändert
        self.sub_p_q_v_info_vector = self.p_q_v_info_vector

        # Jacobimatrix bei Initialiseirung mit Slack-Werten erstellen
        self.J = self.create_jacobian(self.Fk_Ek_vector)
        self.Jk = self.create_sub_jacobian_Jk(self.J)

    # getter und setter
    def get_number_of_voltage_nodes(self):
        return self.__number_of_voltage_nodes

    def init_Fk_Ek_vector(self):

        # Initialisiere Loesungsvektor Fk_Ek(__Fk_Ek_vector) mit Slackknoten-Spannungsstartwerten
        # Spannungsvektor, in Real- und Imaginaerteil (Fk(Fi_init) => Imaginaer und Ek(Ei_init) => Real)

        slack_node = self.__grid_node_list[self.index_of_slack]

        Ei_init, Fi_init = get_cartesian_from_euler(slack_node.get_node_voltage_magnitude(),
                                                    slack_node.get_node_voltage_angle_in_rad())

        init_vector_shape = self.__number_of_nodes * 2
        init_vector = np.ndarray(shape=(init_vector_shape), dtype=float)

        for i in range(self.__number_of_nodes):
            init_vector[i] = Fi_init
            init_vector[i + self.__number_of_nodes] = Ei_init

        return init_vector

    def create_p_q_v_info_vector(self):
        p_values = list()
        q_values = list()
        v_values = list()

        for index, grid_node in enumerate(self.__grid_node_list):
            type_number = grid_node.get_type_number()
            grid_node_type = grid_node.types_index[type_number]

            is_slack_node = grid_node_type == "slack"
            is_voltage_node = grid_node_type == "PV"
            is_load_node = grid_node_type == "PQ"

            if is_slack_node:
                p_value = None
                q_value = None
                v_value = grid_node.get_node_voltage_magnitude() ** 2

                # node_name_and_x_value[0] = Knotenname
                # node_name_and_x_value[1] = Knotentyp
                # node_name_and_x_value[2] = Knotenindex
                # node_name_and_x_value[3] = Elektrische Groeße
                # node_name_and_x_value[4] = Wert der elektrischen Groeße
                node_name_and_p_value = (grid_node.name, grid_node_type, index, "P", p_value)
                node_name_and_q_value = (grid_node.name, grid_node_type, index, "Q", q_value)
                node_name_and_v_value = (grid_node.name, grid_node_type, index, "U", v_value)

                p_values.append(node_name_and_p_value)
                q_values.append(node_name_and_q_value)
                v_values.append(node_name_and_v_value)

            elif is_voltage_node:

                p_value = grid_node.get_p_gen() - grid_node.get_p_load()
                q_value = None
                v_value = grid_node.get_node_voltage_magnitude() ** 2

                node_name_and_p_value = (grid_node.name, grid_node_type, index, "P", p_value)
                node_name_and_q_value = (grid_node.name, grid_node_type, index, "Q", q_value)
                node_name_and_v_value = (grid_node.name, grid_node_type, index, "U", v_value)

                p_values.append(node_name_and_p_value)
                q_values.append(node_name_and_q_value)
                v_values.append(node_name_and_v_value)

            elif is_load_node:

                p_value = -1 * grid_node.get_p_load()
                q_value = -1 * grid_node.get_q_load()
                v_value = None

                node_name_and_p_value = (grid_node.name, grid_node_type, index, "P", p_value)
                node_name_and_q_value = (grid_node.name, grid_node_type, index, "Q", q_value)
                node_name_and_v_value = (grid_node.name, grid_node_type, index, "U", v_value)

                p_values.append(node_name_and_p_value)
                q_values.append(node_name_and_q_value)
                v_values.append(node_name_and_v_value)

        p_info_vector = np.array(p_values, dtype=object)
        q_info_vector = np.array(q_values, dtype=object)
        v_info_vector = np.array(v_values, dtype=object)

        p_q_v_info_vector = np.concatenate((p_info_vector, q_info_vector, v_info_vector), axis=0)

        return p_q_v_info_vector

    """
        Berechnung der Teilmatrizen der Jacobimatrix (J1, J2, J3, J4, J5 und J6)
        Fk_Ek_vector = Voltage vector (Fk = angle at Node k, Ek = magnitude of voltage k)
    """

    def create_jacobian_sub_matrices(self, Fk_Ek_vector):

        self.__has_voltage_nodes = True if self.__number_of_voltage_nodes > 1 else False

        # Initialisierung der Teilmatrizen
        J1, J2, J3, J4, J5, J6 = self.__init_sub_matrices(self.__number_of_nodes, self.__number_of_voltage_nodes + 1)

        # Fuelle Jacobi-Teilmatrizen
        for index, grid_node in enumerate(self.__grid_node_list):

            Fi = Fk_Ek_vector[index]
            Ei = Fk_Ek_vector[index + self.__number_of_nodes]

            for j in range(self.__number_of_nodes):

                # Admittanz aus Knotenadmittanzmatrix speichern
                Yij = self.__bus_admittance_matrix[index][j]
                Gij = Yij.get_real_part()
                Bij = Yij.get_imaginary_part()

                # Diagonalelemente von J1, J2, J3, J4, J5, und J6
                if index == j:
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_dEj, dUi2_dFj, dUi2_dEj = self.__calculate_diag_elements(Ei, Fi, Gij,
                                                                                                            Bij, index)

                # nicht Diagonalelemente von J1, J2, J3, J4, J5, und J6
                else:
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_dEj, dUi2_dFj, dUi2_dEj = self.__calculate_not_diag_elements(Ei, Fi,
                                                                                                                Gij,
                                                                                                                Bij)

                # dim(J1, J2) = Anzahl der Knoten. Hier muss nicht auf den Wert der Laufvariablen index geachtet werden.
                # Wirkleistungselemente
                J1[index][j] = dPi_dFj
                J2[index][j] = dPi_dEj

                # Blindleistungselemente
                J3[index][j] = dQi_dFj
                J4[index][j] = dQi_dEj

                # wenn es Spannungsknoten gibt gilt: dim(J1, J2) = dim(J3, J4) + dim(J5, J6)
                if (J5 is not None) and (J6 is not None):
                    # if index < len(J3):
                    # 	J3[index][j] = dQi_dFj
                    # 	J4[index][j] = dQi_dEj
                    # if index < len(J5):
                    J5[index][j] = dUi2_dFj
                    J6[index][j] = dUi2_dEj
        # else:
        # 	J3[index][j] = dQi_dFj
        # 	J4[index][j] = dQi_dEj

        return J1, J2, J3, J4, J5, J6

    # Initialisierung der Jacobi-Teilmatrizen
    def __init_sub_matrices(self, number_of_nodes, number_of_voltage_nodes):

        # Erstellung der nxn-dimensionalen Numpy-Arrays
        J1 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
        J2 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
        J3 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
        J4 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)

        # wenn Spannungsknoten existieren
        if number_of_voltage_nodes:
            # J5 = np.ndarray(shape=(number_of_voltage_nodes, number_of_nodes), dtype=float)
            # J6 = np.ndarray(shape=(number_of_voltage_nodes, number_of_nodes), dtype=float)
            J5 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
            J6 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
        else:
            J5 = None
            J6 = None

        return J1, J2, J3, J4, J5, J6

    """
        Berechnungsmethoden fuer die Elemente der Jacobi-Teilmatrizen J1, J2, J3, J4, J5 und J6
    """

    # -------------------------------------------------------------------------------------------------------------------

    # Diagonalelement berechnen
    def __calculate_diag_elements(self, Ei, Fi, Gii, Bii, i):

        sum_part_dPi_dFi = sum_part_dPi_dEi = sum_part_dQi_dFi = sum_part_dQi_Ei = 0

        # an dieser Stelle wird fuer die Elemente i != j der Summenanteil berechnet
        for j in range(self.__number_of_nodes):
            if j != i:
                Fj = self.Fk_Ek_vector[j]
                Ej = self.Fk_Ek_vector[j + self.__number_of_nodes]
                Gij = self.__bus_admittance_matrix[i][j].get_real_part()
                Bij = self.__bus_admittance_matrix[i][j].get_imaginary_part()

                sum_part_dPi_dFi += (Fj * Gij + Ej * Bij)
                sum_part_dPi_dEi += (Ej * Gij - Fj * Bij)
                sum_part_dQi_dFi += (Ej * Gij - Fj * Bij)
                sum_part_dQi_Ei += (Fj * Gij + Ej * Bij)

        dPi_dFi = (2 * Fi * Gii) + sum_part_dPi_dFi
        dPi_dEi = (2 * Ei * Gii) + sum_part_dPi_dEi
        dQi_dFi = -2 * Fi * Bii + sum_part_dQi_dFi
        dQi_Ei = -2 * Ei * Bii - sum_part_dQi_Ei
        dUi2_dFi = 2 * Fi
        dUi2_dEi = 2 * Ei

        return dPi_dFi, dPi_dEi, dQi_dFi, dQi_Ei, dUi2_dFi, dUi2_dEi

    # "nicht"-Diagonalelemente berechnen
    def __calculate_not_diag_elements(self, Ei, Fi, Gij, Bij):
        dPi_dFj = ((-1 * Ei) * Bij) + (Fi * Gij)
        dPi_dEj = (Ei * Gij) + (Fi * Bij)
        dQi_dFj = ((-1 * Ei) * Gij) - (Fi * Bij)
        dQi_Ej = ((-1 * Ei) * Bij) + (Fi * Gij)
        dUi2_dFj = 0
        dUi2_dEj = 0
        return dPi_dFj, dPi_dEj, dQi_dFj, dQi_Ej, dUi2_dFj, dUi2_dEj

    # Jacobimatrix mit Teilmatrizen J1 - J6 fuellen
    def create_jacobian(self, Fk_Ek_vector):

        # Untermatrizen der Jacobimatrix
        self.__J1, self.__J2, self.__J3, self.__J4, self.__J5, self.__J6 = self.create_jacobian_sub_matrices(
            Fk_Ek_vector)

        active_load_sub_jacobian = np.hstack((self.__J1, self.__J2))
        reactive_load_sub_jacobian = np.hstack((self.__J3, self.__J4))

        if (self.__J5 is not None) and (self.__J6 is not None):
            voltage_sub_jacobian = np.hstack((self.__J5, self.__J6))
            J = np.vstack((active_load_sub_jacobian, reactive_load_sub_jacobian, voltage_sub_jacobian))
        else:
            J = np.vstack((active_load_sub_jacobian, reactive_load_sub_jacobian))

        return J

    # Unter-Jacobimatrix Jk erstellen in der die Zeilen und Spalten des Slacks nicht mehr enthalten sind und
    # alle Blindleistungsgleichungen aller Spannungsknoten löschen
    def create_sub_jacobian_Jk(self, jacobian_matrix):

        columns_to_delete = list()
        rows_to_delete = list()

        for index, item in enumerate(self.p_q_v_info_vector):
            # item[0] = Knotenname
            # item[1] = Knotentyp
            # item[2] = Knotenindex
            # item[3] = Elektrische Groeße
            # item[4] = Wert der elektrischen Groeße
            grid_node_type = item[1]
            value_type = item[3]

            if grid_node_type == "slack":
                columns_to_delete.append(index)
                rows_to_delete.append(index)
            elif (grid_node_type == "PV" and value_type == "Q") or (
                    grid_node_type == "PQ" and value_type == "U"):
                rows_to_delete.append(index)

        # Zeilen und Spalten loeschen
        self.sub_p_q_v_info_vector = np.delete(self.p_q_v_info_vector, rows_to_delete, 0)
        Jk = np.delete(jacobian_matrix, rows_to_delete, 0)
        Jk = np.delete(Jk, columns_to_delete, 1)

        return Jk

    def get_indices_of_voltage_nodes(self):

        indices_of_voltage_nodes = list()

        for index, grid_node in enumerate(self.__grid_node_list):
            # fuer jeden Spannungsknoten
            if grid_node.get_type_number() == grid_node.get_grid_node_type_index_of("PV"):
                indices_of_voltage_nodes.append(index)

        return indices_of_voltage_nodes

    def get_sub_Fk_Ek_vector(self, Fk_Ek_vector):
        sub_Fk_Ek_vector = np.delete(Fk_Ek_vector, self.index_of_slack, 0)
        sub_Fk_Ek_vector = np.delete(sub_Fk_Ek_vector, ((self.index_of_slack - 1) + self.__number_of_nodes),
                                     0)

        return sub_Fk_Ek_vector
