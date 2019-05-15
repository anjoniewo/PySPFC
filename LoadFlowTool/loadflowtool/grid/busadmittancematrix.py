import numpy as np
from LoadFlowTool.loadflowtool.grid.admittance import Admittance
import copy


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
    def __get_sum_of_grid_lines_on_node(self, node_name_i, node_name_j):

        # Summenadmittanz an Knoten i und entspricht einem Element der Knotenadmittanzmatrix (KAM)
        sum_admittance = Admittance(g=0, b=0)

        # Ist Diagonalelement ?
        is_diag_elem = node_name_i == node_name_j

        for grid_line in self.__grid_line_list:

            # echte Kopien der Längs- und Queradmittanz erzeugen
            grid_line_admittance = copy.deepcopy(grid_line.get_admittance())
            grid_line_transverse_admittance = copy.deepcopy(grid_line.get_transverse_admittance_on_node())

            # pruefen ob Leitung beide Knoten verbidnet
            is_connecting_i_j = grid_line.get_node_name_i() == node_name_i and \
                                grid_line.get_node_name_j() == node_name_j or \
                                grid_line.get_node_name_i() == node_name_j and \
                                grid_line.get_node_name_j() == node_name_i

            # Prüfen ob Diagonalelement
            if is_diag_elem:
                # Addiere Längsadmittanz von Gridline zur Summenadmittanz
                sum_admittance += grid_line_admittance
                # Prüfen ob Queradmittanz in Gridline vorhanden
                if grid_line.get_transverse_admittance_on_node():
                    # Addiere Knoten-Queradmittanz von Gridline zur Summenadmittanz
                    sum_admittance += grid_line_transverse_admittance
            else:
                if is_connecting_i_j:
                    # Addiere Längsadmittanz von Gridline zur Summenadmittanz
                    sum_admittance += grid_line_admittance

        return sum_admittance if is_diag_elem else sum_admittance * -1

    # Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
    def calc_matrix(self, grid_node_list, grid_line_list):

        # quadratische Matrixdimension: nxn
        number_of_grid_nodes = len(grid_node_list)

        # Erstellung eines nxn-dimensionalen Numpy-Arrays
        self.matrix = np.ndarray(shape=(number_of_grid_nodes, number_of_grid_nodes), dtype=object)

        for index, grid_node in enumerate(grid_node_list):

            # Setzen der gefilterten Leitungsliste
            grid_line_list_with_node_name = [grid_line for grid_line in grid_line_list if
                                               grid_line.get_node_name_i() == grid_node.get_name() or
                                               grid_line.get_node_name_j() == grid_node.get_name()]

            self.__grid_line_list = copy.deepcopy(grid_line_list_with_node_name)

            for j in range(index, number_of_grid_nodes):
                gridnode_name_j = grid_node_list[j].get_name()

                self.matrix[index][j] = self.matrix[j][index] = self.__get_sum_of_grid_lines_on_node(
                    grid_node.get_name(),
                    gridnode_name_j)
