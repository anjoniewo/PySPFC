"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Lastflussberechnung - Newton-Raphson-Verfahren
Seiten:  80

Fuer Referenz- (Slack) und Lastknoten (P-Q) gelten folgende Gleichungen:
Summe ueber alle mit dem Knoten verbundenen Knoten ->

Si = Pi + jQi
Pi = ∑  (Ei * (Ej * Gij - Fj * Bij) + Fi * (Fj * Gij + Ej * Bij))
Qi = ∑  (Fi * (Ej * Gij - Fj * Bij) - Ei * (Fj * Gij + Ej * Bij))

Fuer spannungsgeregelte Knoten (P-U) gilt:

Ui^2 = Ei^2 + Fi^2

Definitionen:

Ui = Ei + jFi
Ei = Re{Ui}
Fi = Im{Ui}
Yi = Gi + jBi
Gi = Re{Yi}
Bi = Im{Yi}

"""

import copy


class LoadFlowEquations:

    def __init__(self, grid_line_list=list(), grid_node_list=list()):
        self.__grid_line_list = copy.deepcopy(grid_line_list)

        self.__grid_node_list = copy.deepcopy(grid_node_list)

        self.__active_load_equations = list()

        self.__reactive_load_equations = list()
