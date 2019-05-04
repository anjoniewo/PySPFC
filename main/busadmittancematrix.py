import numpy as np
from main.admittance import Admittance


# Klasse fuer die Erstellung der Knotenadmittanzmatrix
class BusAdmittanceMatrix:

    # Initialisierungskonstruktor
    def __init__(self):
        self.matrix = None

        # Gridlineliste (Leitungsliste)
        self.__grid_line_list = ()

    # Methode zur Aufsummierung aller Admittanzen an einem Knoten
    # Parameter:
    # Knotennamen,
    # [Optional] Modus: True|False (all_admittances), Wenn True: werden alle Laengs- und Queradmittanzen aufsummiert. Wenn False: werden nur die Längsadmittanzen aufsummiert (Queradmittanzen werden igoniert)
    # Rückgabewert: kummulierter Admittanzenwert
    # Quelle: E. Handschin, Elektrische Energieübertragungssysteme. Teil 1: Stationaerer Betriebszustand. Heidelberg: Hueting, 1983, Seite 51
    def __get_sum_of_grid_lines_on_node(self, node_name, get_all_admittances_on_node=True):

        # Summenadmittanz an Knoten i und entspricht einem Element der Knotenadmittanzmatrix (KAM)
        sum_admittance = Admittance()

        for grid_line in self.__grid_line_list:

            if node_name == grid_line.get_node_name_i() or node_name == grid_line.get_node_name_j():

                # Addiere Längsadmittanz von Gridline zur Summenadmittanz (für Diagonal- und Nichtdiagonal-Elemente der KAM)
                sum_admittance.addition(grid_line.get_admittance())

                # Prüfen ob Modus "alle Admittanzen" true ist und ob Queradmittanz in Gridline vorhanden
                if get_all_admittances_on_node and grid_line.get_transverse_admittance_on_node():

                    # Addiere Knoten-Queradmittanz von Gridline zur Summenadmittanz (nur für Nichtdiagonal-Elemente der KAM)
                    sum_admittance.addition(grid_line.get_transverse_admittance_on_node())

        return sum_admittance

    # Methode zur Erstellung der Knotenpunkt-Admittanz Matrix
    def calc_matrix(self, grid_node_list, grid_line_list):

        # Setzen der Addmitanzliste
        self.__grid_line_list = grid_line_list

        # quadratische Matrixdimension: nxn
        n = len(grid_node_list)

        # Erstellung eines nxn-dimensionalen Numpy-Arrays
        self.matrix = np.ndarray(shape=(n, n), dtype=object)

        for i in range(0, n):
            for j in range(i, n):

                # Diagonalelemente der Matrix i=j
                if i == j:
                    self.matrix[i][j] = self.__get_sum_of_grid_lines_on_node(grid_node_list[i].get_name())

                # Nicht-Diagonalelemente der Matrix i≠j
                else:
                    admittance_elem = self.__get_sum_of_grid_lines_on_node(grid_node_list[i].get_name(), False)

                    if admittance_elem.get_g() is not None:
                        admittance_elem.set_g(admittance_elem.get_g() * -1)

                    if admittance_elem.get_b() is not None:
                        admittance_elem.set_b(admittance_elem.get_b() * -1)

                    self.matrix[i][j] = admittance_elem
