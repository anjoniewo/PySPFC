"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Lastflussberechnung - Newton-Raphson-Verfahren
Seiten:  80

Aus der Jakobimatrix J werden die Gleichungen des Slackknotens gestrichen:

=> dim(J) = (m, m) -> dim(Jk) = (m-2, m-2)

Aufbau der Jakobimatrix J:
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
import numpy as np


class JacobianMatrix:

    def __init__(self, grid_node_list, bus_admittance_matrix):

        # Liste der Netzknoten
        self.__grid_node_list = grid_node_list

        # Anzahl an Netzknoten
        self.__number_of_nodes = len(self.__grid_node_list)

        # Knotenadmittanzmatrix
        self.__bus_admittance_matrix = bus_admittance_matrix

        # Spannungsvektor, in Real- und Imaginaerteil (Fk => Imaginaer und Ek => Real)
        self.__Fk_Ek_vector = self.init_Fk_Ek_vector(E0=1)

        # Untermatrizen der Jakobimatrix
        self.__J1, self.__J2, self.__J3, self.__J4, self.__J5, self.__J6, index_of_slack = self.__create_jacobian_sub_matrices()

        self.J = self.create_jacobian()
        self.Jk = self.create_sub_jacobian_Jk(index_of_slack)

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

        # Dimension der Teilmatrizen fuer Spannungsknoten
        n_voltage = len(list_of_voltage_nodes)

        # Initialisierung der Teilmatrizen
        J1, J2, J3, J4, J5, J6 = self.__init_sub_matrices(n, n_voltage)

        index_of_slack = None

        for i in range(0, self.__number_of_nodes):
            if index_of_slack is None:
                index_of_slack = i if self.__grid_node_list[i].get_type_number() == 0 else None
            Fi = self.__Fk_Ek_vector[i]
            Ei = self.__Fk_Ek_vector[i + self.__number_of_nodes]
            for j in range(0, self.__number_of_nodes):

                # Admittanz aus Knotenadmittanzmatrix speichern
                Yij = self.__bus_admittance_matrix[i][j]
                Gij = Yij.get_real_part()
                Bij = Yij.get_imaginary_part()

                # Diagonalelemente von J1, J2, J3, J4, J5, und J6
                if i == j:
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_dEj, dUi2_dFj, dUi2_dEj = self.calculate_diag_elements(Ei, Fi, Gij,
                                                                                                          Bij, i)

                # nicht Diagonalelemente von J1, J2, J3, J4, J5, und J6
                else:
                    dPi_dFj, dPi_dEj, dQi_dFj, dQi_dEj, dUi2_dFj, dUi2_dEj = self.calculate_not_diag_elements(Ei, Fi,
                                                                                                              Gij,
                                                                                                              Bij)

                # dim(J1, J2) = Anzahl der Knoten. Hier muss nicht auf den Wert der Laufvariablen i geachtet werden.
                J1[i][j] = dPi_dFj
                J2[i][j] = dPi_dEj

                # wenn es Spannungsknoten gibt gilt: dim(J1, J2) = dim(J3, J4) + dim(J5, J6)
                if (J5 is not None) and (J6 is not None):
                    if i < len(J3):
                        J3[i][j] = dQi_dFj
                        J4[i][j] = dQi_dEj
                    if i < len(J5):
                        J5[i][j] = dUi2_dFj
                        J6[i][j] = dUi2_dEj
                else:
                    J3[i][j] = dQi_dFj
                    J4[i][j] = dQi_dEj

        return J1, J2, J3, J4, J5, J6, index_of_slack

    # Initialisierung der Teilmatrizen
    def __init_sub_matrices(self, number_of_nodes, number_of_voltage_nodes):

        # Erstellung der nxn-dimensionalen Numpy-Arrays

        J1 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
        J2 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)

        # wenn Spannungsknoten existieren
        if number_of_voltage_nodes:
            J3 = np.ndarray(
                shape=(number_of_nodes - number_of_voltage_nodes, number_of_nodes),
                dtype=float)
            J4 = np.ndarray(
                shape=(number_of_nodes - number_of_voltage_nodes, number_of_nodes),
                dtype=float)
            J5 = np.ndarray(shape=(number_of_voltage_nodes, number_of_nodes), dtype=float)
            J6 = np.ndarray(shape=(number_of_voltage_nodes, number_of_nodes), dtype=float)
        else:
            J3 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
            J4 = np.ndarray(shape=(number_of_nodes, number_of_nodes), dtype=float)
            J5 = None
            J6 = None

        return J1, J2, J3, J4, J5, J6

    """
        Berechnungsmethoden fuer die Elemente der Teiljakobimatrizen J1, J2, J3, J4, J5 und J6
    """

    # -------------------------------------------------------------------------------------------------------------------

    # Diagonalelement berechnen
    def calculate_diag_elements(self, Ei, Fi, Gii, Bii, i):

        sum_part_dPi_dFi = sum_part_dPi_dEi = sum_part_dQi_dFi = sum_part_dQi_Ei = 0

        for j in range(0, self.__number_of_nodes):
            if j != i:
                Fj = self.__Fk_Ek_vector[j]
                Ej = self.__Fk_Ek_vector[j + self.__number_of_nodes]
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

    # nicht Diagonalelement berechnen
    def calculate_not_diag_elements(self, Ei, Fi, Gij, Bij):
        dPi_dFj = ((-1 * Ei) * Bij) + (Fi * Gij)
        dPi_dEj = (Ei * Gij) + (Fi * Bij)
        dQi_dFj = ((-1 * Ei) * Gij) - (Fi * Bij)
        dQi_Ej = ((-1 * Ei) * Bij) + (Fi * Gij)
        dUi2_dFj = 0
        dUi2_dEj = 0
        return dPi_dFj, dPi_dEj, dQi_dFj, dQi_Ej, dUi2_dFj, dUi2_dEj

    # Jakobi-Matrix mit Teilmatrizen J1 - J6 fuellen
    def create_jacobian(self):

        active_load_sub_jacobian = np.hstack((self.__J1, self.__J2))
        reactive_load_sub_jacobian = np.hstack((self.__J3, self.__J4))

        if (self.__J5 is not None) and (self.__J6 is not None):
            voltage_sub_jacobian = np.hstack((self.__J5, self.__J6))
            J = np.vstack((active_load_sub_jacobian, reactive_load_sub_jacobian, voltage_sub_jacobian))
        else:
            J = np.vstack((active_load_sub_jacobian, reactive_load_sub_jacobian))

        det_of_J = np.linalg.det(J)

        return J if det_of_J == 0.0 else None

    # Unter-Jakobi-Matrix Jk erstellen in der die Zeilen und Spalten des Slacks nicht mehr enthalten sind
    def create_sub_jacobian_Jk(self, index_of_slack):

        # Zeilen des Slack loeschen
        Jk = np.delete(self.J, index_of_slack, 0)
        Jk = np.delete(Jk, ((index_of_slack - 1) + self.__number_of_nodes), 0)

        # Spalten des Slack loeschen
        Jk = np.delete(Jk, index_of_slack, 1)
        Jk = np.delete(Jk, ((index_of_slack - 1) + self.__number_of_nodes), 1)

        det_of_Jk = np.linalg.det(Jk)

        return Jk
