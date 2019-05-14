"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Lastflussberechnung - Newton-Raphson-Verfahren
Seiten:  80

Aus der Jakobimatrix J werden die Gleichungen des Slackknotens gestrichen:

=> dim(J) = (m, m) -> dim(Jk) = (m-2, m-2)

Aufbau der Unter-Jakobimatrix Jk:
	
			 |                     |                    |    | ΔF2 |     | ΔP2 |
			 |                     |                    |    |  .  |     |     |
			 |    Jk1 = δPi/δFj    |   Jk2 = δPi/δEj    |    |  .  |     |     |
			 |                     |                    |    |  .  |     |     |
			 |                     |                    |    | ΔFn |     | ΔPn |
	[Jk] =>  |------------------------------------------|  * |-----|  =  |-----|
			 |                     |                    |    | ΔE2 |     | ΔQ2 |
			 |                     |                    |    |  .  |     |     |
			 |   Jk3 = δQi/δFj     |    Jk4 = δQi/δEj   |    |  .  |     |     |
			 |                     |                    |    |  .  |     |     |
			 |                     |                    |    | ΔEn |     | ΔQn |

Teilmatrix J_3:
Für Elemente außerhalb der Diagonalen gilt:

    δQi/δFj = -E_i * G_ij - F_i * B_ij (für i,j = 1, 2, ..., n aber i != j)

Für die Diagonalelemente gilt:

    δQi/δFi = -2 * F_i * B_ii +  ∑ (E_j * G_ij - F_j * B_ij) (Summe j = 1 bis n ohne j = i)

Teilmatrix J_4:
Für Elemente außerhalb der Diagonalen gilt:

    δQi/δEj = -E_i * B_ij + F_i * G_ij (für i,j = 1, 2, ..., n aber i != j)

Für die Diagonalelemente gilt:

    δQi/δEi = -2 * E_i * B_ii +  ∑ (F_j * G_ij + E_j * B_ij) (Summe j = 1 bis n ohne j = i)
"""

import numpy as np


class JacobianMatrix:

    def __init__(self, grid_node_list, bus_admittance_matrix):

        self.__grid_node_list = grid_node_list
        self.__number_of_nodes = len(self.__grid_node_list)
        self.__bus_admittance_matrix = bus_admittance_matrix
        self.__Fk_Ek_vector = self.init_Fk_Ek_vector()

        # sub-Matrix J1
        self.__J1, self.__J2, self.__J3, self.__J4, self.__J5, self.__J6 = self.__create_jacobian_sub_matrices()

    def init_Fk_Ek_vector(self, F0=0, E0=230):

        init_vector = np.zeros(2 * self.__number_of_nodes)

        for i in range(0, self.__number_of_nodes):
            init_vector[i] = F0
            init_vector[i + self.__number_of_nodes] = E0

        return init_vector

    # Berechnung der Teilmatrizen der Jakobimatrix (J1, J2, J3, J4, J5 und J6)
    def __create_jacobian_sub_matrices(self):

        # quadratische Matrixdimension: NxN
        n = self.__number_of_nodes

        # gefilterte Liste mit Spannungsknoten
        list_of_voltage_nodes = [grid_node for grid_node in self.__grid_node_list if grid_node.get_type_number() == 2]

        # Dimesnion der Teilmatrizen fuer Spannungsknoten
        n_voltage = len(list_of_voltage_nodes)

        # Initialisierung der Teilmatrizen
        J1, J2, J3, J4, J5, J6 = self.__init_sub_matrices(n, n_voltage)

        for i in range(0, self.__number_of_nodes):
            Fi = self.__Fk_Ek_vector[i]
            Ei = self.__Fk_Ek_vector[i + self.__number_of_nodes]
            for j in range(0, self.__number_of_nodes):

                # Admittanz aus Knotenadmittanzmatrix speichern
                Yij = self.__bus_admittance_matrix[i][j]

                # Diagonalelemente von J1
                if i == j:
                    Gij = Yij.get_imaginary_part()
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_Ej, dUi2_dFj, dUi2_dEj = self.calculate_diag_elements(Fi, Gij, i)
                # nicht Diagonalelemente von J1
                else:
                    Gij = Yij.get_real_part()
                    Bij = Yij.get_imaginary_part()
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_dEj, dUi2_dFj, dUi2_dEj = self.calculate_not_diag_elements(Ei, Fi,
                                                                                                              Gij,
                                                                                                              Bij)

                J1[i][j] = dPi_dFj
                J2[i][j] = dPi_dEj
                J3[i][j] = dQi_dFj
                J4[i][j] = dQi_dEj

                if J5 and J6:
                    J5[i][j] = dUi2_dFj
                    J6[i][j] = dUi2_dEj

        return J1, J2, J3, J4, J5, J6

    # Initialisierung der Teilmatrizen
    def __init_sub_matrices(self, number_of_nodes, number_of_voltage_nodes):

        # Erstellung der nxn-dimensionalen Numpy-Arrays

        J1 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=object)
        J2 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=object)

        # wenn Spannungsknoten existieren
        if number_of_voltage_nodes:
            J3 = np.ndarray(
                shape=(number_of_nodes - number_of_voltage_nodes, number_of_nodes - number_of_voltage_nodes),
                dtype=object)
            J4 = np.ndarray(
                shape=(number_of_nodes - number_of_voltage_nodes, number_of_nodes - number_of_voltage_nodes),
                dtype=object)
            J5 = np.ndarray(shape=(number_of_voltage_nodes, number_of_voltage_nodes), dtype=object)
            J6 = np.ndarray(shape=(number_of_voltage_nodes, number_of_voltage_nodes), dtype=object)
        else:
            J3 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=object)
            J4 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=object)
            J5 = None
            J6 = None

        return J1, J2, J3, J4, J5, J6


"""
    Berechnungsmethoden fuer die Elemente der Teiljakobimatrizen J1, J2, J3, J4, J5 und J6
"""


# -------------------------------------------------------------------------------------------------------------------

# Diagonalelement berechnen
def calculate_diag_elements(self, Fi, Gii, i):
    sum_part_dPi_dFj = 0
    sum_part_dPi_dEj = 0
    sum_part_dQi_dFj = 0
    sum_part_dQi_Ej = 0
    sum_part_dUi2_dFj = 0
    sum_part_dUi2_dEj = 0

    for j in range(0, self.__number_of_nodes):
        if j != i:
            Fj = self.__Fk_Ek_vector[j]
            Ej = self.__Fk_Ek_vector[j + self.__number_of_nodes]
            Gij = self.__bus_admittance_matrix[i][j].get_real_part()
            Bij = self.__bus_admittance_matrix[i][j].get_imaginary_part()

            sum_part_dPi_dFj += (Fj * Gij + Ej * Bij)
            sum_part_dPi_dEj += 0
            sum_part_dQi_dFj += 0
            sum_part_dQi_Ej += 0
            sum_part_dUi2_dFj += 0
            sum_part_dUi2_dEj += 0

    dPi_dFj = 2 * Fi * Gii + sum_part_dPi_dFj
    dPi_dEj = 0
    dQi_dFj = 0
    dQi_Ej = 0
    dUi2_dFj = 0
    dUi2_dEj = 0

    return dPi_dFj, dPi_dEj, dQi_dFj, dQi_Ej, dUi2_dFj, dUi2_dEj


# nicht Diagonalelement berechnen
def calculate_not_diag_elements(self, Ei, Fi, Gij, Bij):
    dPi_dFj = (-1 * Ei) * Bij + Fi * Gij
    dPi_dEj = 0
    dQi_dFj = 0
    dQi_Ej = 0
    dUi2_dFj = 0
    dUi2_dEj = 0
    return dPi_dFj, dPi_dEj, dQi_dFj, dQi_Ej, dUi2_dFj, dUi2_dEj
