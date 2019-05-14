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


Teilmatrix J_2:
Für Elemente außerhalb der Diagonalen gilt:

    δPi/δEj = E_i * G_ij + F_i * B_ij (für i,j = 1, 2, ..., n aber i != j)

Für die Diagonalelemente gilt:

    δPi/δEi = 2 * E_i * G_ii +  ∑ (E_j * G_ij - F_j * B_ij) (Summe j = 1 bis n ohne j = i)

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
        self.__bus_admittance_matrix = bus_admittance_matrix
        self.__Fk_Ek_vector = np.array()

    def init_Fk_Ek_vector(self, F0, E0):

        for i in range(0, len(self.__grid_node_list)):
            self.__Fk_Ek_vector[i] = 0
            self.__Fk_Ek_vector[i + ]

    # Methode bastelt J1
    def create_jacobian_J1(self):

        # quadratische Matrixdimension: NxN
        n = len(self.__grid_node_list)

        # Erstellung eines nxn-dimensionalen Numpy-Arrays
        J1 = np.ndarray(shape=(n, n), dtype=object)

        """
             Teilmatrix J_1 mit dim(J_1) = (N, N):
             
            Für Elemente außerhalb der Diagonalen gilt:

            δPi/δFj = -E_i * B_ij + F_i * G_ij (für i,j = 0, 1, ..., n aber i != j)

            Für Diagonalelemente gilt:

            δPi/δFi = 2 * F_i * G_ii +  ∑ (F_j * G_ij + E_j * B_ij) (Summe j = 0 bis n ohne j = i)

        """

        Ei = 0
        Ej = 0
        Fi = 0
        Fj = 0
        Gij = 0
        Bij = 0

        dPi_dFj = 0

        for i in range(0, len(self.__sub_grid_node_list)):
            Ei =
            for j in range(0, len(self.__sub_grid_node_list)):

                if i == j:
                    self.__Ei =
                    dPi_dFj = calculate_diag_of_J1()
                else:
                    dPi_dFj = -1 * Ei * Bij + Fi * Bij

