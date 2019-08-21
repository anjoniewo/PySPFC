import math

"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Stationäres Netzmodell
Seite:   56

-------------------------------------------------------------------------------------------
Knotenart       | Typ |   Spezifizierte Groeße            | Unbekannte Groeße | Typnumber |
-------------------------------------------------------------------------------------------
Referenzknoten  |Slack|   U_1, δ_1, P_L1, Q_L1            |     P_G1, Q_G1    |     1     |
-------------------------------------------------------------------------------------------
Lastknoten      | PQ  |   P_Gi = 0, Q_Gi = 0, P_Li, Q_Li  |     U_i, δ_i      |     2     |
-------------------------------------------------------------------------------------------
Einspeisung     | PV  |   P_Gi, U_i, P_Li, Q_Li           |     Q_Gi, δ_i     |     3     |
-------------------------------------------------------------------------------------------
"""

Q_MIN_DEFAULT = 1000
Q_MAX_DEFAULT = 1000


class GridNode:
    """
        Objects to define gridelements nodes of a network
        generators and loads are connected to gridelements node
        in which the sum of loads and generators represent the electrical parameters of a gridelements node
    """

    # Initialisierungs-Konstruktor
    def __init__(self, name, **kwargs):

        # ***** Knotenname *****
        self.__name = name

        self.__generators = kwargs['generators'] if 'generators' in kwargs else None

        self.__loads = kwargs['loads'] if 'loads' in kwargs else None

        # **********************
        # ***** Knotentyp  *****
        # **********************
        # 0 = slack-Knoten (Referenzknoten)
        # 1 = PQ-Knoten (Lastknoten)
        # 2 = PV-Knoten (Einspeisung)
        self.types_index = {1: "slack", 2: "PQ", 3: "PV"}
        self.__types = {"slack": 1, "PQ": 2, "PV": 3}
        # default value 2 => PQ
        self.__typenumber = kwargs['typenumber'] if 'typenumber' in kwargs else 2

        # ***********************
        # **** Lastparameter ****
        # ***********************
        # Wirkleistung in kW
        self.__p_load = kwargs['p_load'] if 'p_load' in kwargs else None
        # Blindleistung in kVar
        self.__q_load = kwargs['q_load'] if 'q_load' in kwargs else None

        # ***********************
        # ***** Einspeisung *****
        # ***********************
        # Wirkleistung in kW
        self.__p_gen = kwargs['p_gen'] if 'p_gen' in kwargs else None
        # Blindleistung in kVar
        self.__q_gen = kwargs['q_gen'] if 'q_gen' in kwargs else None

        # Leistungsgrenzen eines Knotens wenn Einspeiser am Knoten
        self.__p_min = kwargs['p_min'] if 'p_min' in kwargs else None
        self.__p_max = kwargs['p_max'] if 'p_max' in kwargs else None

        self.__q_min = kwargs['q_min'] if 'q_min' in kwargs else Q_MIN_DEFAULT
        self.__q_max = kwargs['q_max'] if 'q_max' in kwargs else Q_MAX_DEFAULT

        # ***************************
        # ***** Spannungswinkel *****
        # ***************************
        self.__theta = kwargs['v_angle'] if 'v_angle' in kwargs else None

        # **************************
        # ***** Knotenspannung *****
        # **************************
        self.__node_voltage = kwargs['v_mag'] if 'v_mag' in kwargs else None

    # Knotenparameter setzen
    # self.set_node_parameters(node_parameters)

    # getter-Methoden
    def __get_name(self):
        return self.__name

    def __get_generators(self):
        return self.__generators

    def __get_loads(self):
        return self.__loads

    def get_type_number(self):
        return self.__typenumber

    def get_p_load(self):
        return self.__p_load

    def get_q_load(self):
        return self.__q_load

    def get_p_gen(self):
        return self.__p_gen

    def get_q_gen(self):
        return self.__q_gen

    def get_q_min(self):
        return self.__q_min

    def get_q_max(self):
        return self.__q_max

    def get_grid_node_type_index_of(self, node_type):
        return self.__types[node_type]

    # Methode gibt den Betrag der Spannungsggroeße zurück
    def get_node_voltage_magnitude(self):
        return self.__node_voltage

    # Methode gibt den Spannungswinkel in Bogenmaß zurück
    def get_node_voltage_angle_in_rad(self):
        return self.__theta

    # Methode gibt den Spannungswinkel in Bogenmaß zurück
    def get_node_voltage_angle_in_grad(self):
        return self.__theta * (180 / math.pi)

    # setzt die Typenumber um nachtraeglich aus PU-Knoten, PQ-Knoten machen zu koennen
    def set_typenumber(self, typenumber):
        self.__typenumber = typenumber

    def set_q_load(self, q_load):
        self.__q_load = q_load

    def set_generators(self, generators):
        self.__generators = generators

    def set_loads(self, loads):
        self.__loads = loads

    name = property(__get_name)
    generators = property(__get_generators)
    loads = property(__get_loads)

    # # Methode setzt die Knotenparameter in Abhaengigkeit des Knotentyps
    # def set_node_parameters(self, node_parameters):
    #
    #     # Fuer alle Knotentypen
    #     # ***********************
    #     # **** Lastparameter ****
    #     # ***********************
    #     # Wirkleistung in kW
    #     # Fuer alle Knotentypen (Last) Wirkleistung in kW
    #     self.__p_load = node_parameters[0]
    #
    #     # Fuer alle Knotentypen (Last) Blindleistung in kVar
    #     self.__q_load = node_parameters[1]
    #
    #     # Slack-Knoten (Referenzknoten)
    #     # setzen von: Knotenspannung (node_voltage) in kV, Spannungswinkel (theta) in Bogenmaß
    #     if self.__typenumber == self.get_grid_node_type_index_of("slack"):
    #         # Spannungsbetrag
    #         self.__node_voltage = node_parameters[5]
    #         self.__theta = node_parameters[4]
    #         self.__p_min = node_parameters[6]
    #         self.__p_max = node_parameters[7]
    #         self.__q_min = node_parameters[8]
    #         self.__q_max = node_parameters[9]
    #
    #     # P-U-Knoten (Einspeisung)
    #     # setzen von : Wirkleistung in kW (active_injection_power), Knotenspannung (node_voltage) in kV
    #     elif self.__typenumber == self.get_grid_node_type_index_of("voltage"):
    #         self.__p_gen = node_parameters[2]
    #         self.__node_voltage = node_parameters[5]
    #         self.__p_min = node_parameters[6]
    #         self.__p_max = node_parameters[7]
    #         self.__q_min = node_parameters[8]
    #         self.__q_max = node_parameters[9]
    #     else:
    #         ERROR = ""

    # Bildschirmausgabe der Knotenparameter
    def __str__(self):
        result = ""
        result += "\n\n------------------------------------"
        result += "\nKnotenbezeichnung: " + str(self.__name)
        result += "\nKnotentyp: " + str(self.types_index[self.__typenumber])

        if self.__p_gen:
            result += "\n\nEinspeisung:"
            result += "\nWirkleistung P = " + str(self.__p_gen) + " kW"
            result += "\nBlindleistung Q = " + str(self.__q_gen) + " kVar"

        if self.__p_load:
            result += "\n\nLast:"
            result += "\nWirkleistung P = " + str(self.__p_load) + " kW"
            result += "\nBlindleistung Q = " + str(self.__q_load) + " kVar"

        if self.__node_voltage:
            result += "\n\nSpannung am Knoten: " + str(self.__node_voltage) + " kV"
            result += "\nSpannungswinkel: " + str(self.__theta) + "°"

        return result
