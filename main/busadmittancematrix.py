import numpy as np
from main.admittance import Admittance


# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:

    # Initialisierungskonstruktor
    def __init__(self):
        self.matrix = None

        # Gridlineliste (Leitungsliste)
        self.__grid_line_list = list()

    # Methode zur Aufsummierung aller Admittanzen an einem Knoten
    # Parameter:
    # Knotennamen,
    # [Optional] Modus: True|False (all_admittances), Wenn True: werden alle Laengs- und Queradmittanzen aufsummiert. Wenn False: werden nur die Längsadmittanzen aufsummiert (Queradmittanzen werden igoniert)
    # Rückgabewert: kummulierter Admittanzenwert
    # Quelle: E. Handschin, Elektrische Energieübertragungssysteme. Teil 1: Stationaerer Betriebszustand. Heidelberg: Hueting, 1983, Seite 51
    def __get_sum_of_grid_lines_on_node(self, index_i, index_j, node_name_i, node_name_j):

        # Summenadmittanz an Knoten i und entspricht einem Element der Knotenadmittanzmatrix (KAM)
        sum_admittance = Admittance()

        # Pruefung ob Diagonalelement
        is_diagonal_element = node_name_i == node_name_j

        for grid_line in self.__grid_line_list:

            # Pruefen ob grid_line mit Knoten verbunden ist
            is_line_at_node = node_name_i == grid_line.get_node_name_i() or node_name_i == grid_line.get_node_name_j()

            if is_line_at_node:

                # Pruefen ob grid_line die Knoten node_name_i und node_name_j verbindet
                is_connection = grid_line.get_node_name_i() == node_name_i and \
                                grid_line.get_node_name_j() == node_name_j or \
                                grid_line.get_node_name_i() == node_name_j and \
                                grid_line.get_node_name_j() == node_name_i

                if is_connection:
                    # Addiere Längsadmittanz von Gridline zur Summenadmittanz (für Diagonal- und Nichtdiagonal-Elemente)
                    sum_admittance += grid_line.get_admittance()

                elif is_diagonal_element:
                    # Addiere Knoten-Queradmittanz von Gridline zur Summenadmittanz (nur für Nichtdiagonal-Elemente)
                    sum_admittance += grid_line.get_admittance() + grid_line.get_transverse_admittance_on_node()

        return sum_admittance if is_diagonal_element else sum_admittance * -1

    # Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
    def calc_matrix(self, grid_node_list, grid_line_list):

        # Setzen der Addmitanzliste
        self.__grid_line_list = grid_line_list

        # quadratische Matrixdimension: nxn
        n = len(grid_node_list)

        # Erstellung eines nxn-dimensionalen Numpy-Arrays
        self.matrix = np.ndarray(shape=(n, n), dtype=object)

        for i in range(0, n):
            gridnode_name_i = grid_node_list[i].get_name()
            for j in range(i, n):
                gridnode_name_j = grid_node_list[j].get_name()

                self.matrix[i][j] = self.__get_sum_of_grid_lines_on_node(i, j, gridnode_name_i, gridnode_name_j)

                if i != j:
                    symmetric_elem = self.matrix[i][j]
                    self.matrix[j][i] = symmetric_elem

                # if i == j:
                #     # Diagonalelemente der Matrix i=j
                #     self.matrix[i][j] = self.__get_sum_of_grid_lines_on_node(gridnode_name_i)
                #
                # # Nicht-Diagonalelemente der Matrix i≠j
                # else:
                #     admittance_elem = self.__get_sum_of_grid_lines_on_node(gridnode_name_i)
                #
                #     if admittance_elem.get_real_part() is not None:
                #         admittance_elem.set_real_part(admittance_elem.get_real_part() * -1)
                #
                #     if admittance_elem.get_imaginary_part() is not None:
                #         admittance_elem.set_imaginary_part(admittance_elem.get_imaginary_part() * -1)
                #
                #     # Matrix ist symmetrisch
                #     self.matrix[i][j] = admittance_elem
                #     self.matrix[j][i] = admittance_elem
