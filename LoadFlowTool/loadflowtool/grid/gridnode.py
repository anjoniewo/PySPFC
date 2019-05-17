"""
Quelle:  E. Handschin, "Elektrische Energieübertragunssysteme",
         Teil 1: Stationärer Betriebszustand
Kapitel: Stationäres Netzmodell
Seite:   56

-------------------------------------------------------------------------------
Knotenart       | Typ |   Spezifizierte Groeße            | Unbekannte Groeße |
-------------------------------------------------------------------------------
Referenzknoten  |Slack|   U_1, δ_1, P_L1, Q_L1            |     P_G1, Q_G1    |
-------------------------------------------------------------------------------
Lastknoten      | P-Q |   P_Gi = 0, Q_Gi = 0, P_Li, Q_Li  |     U_i, δ_i      |
-------------------------------------------------------------------------------
Einspeisung     | P-U |   P_Gi, U_i, P_Li, Q_Li|Q_Gi, δ_i |     Q_Gi, δ_i     |
-------------------------------------------------------------------------------


"""


# ein Knoten ist ein Netzelement an einem bestimmten Punkt im Netz
class GridNode:

    # Initialisierungs-Konstruktor
    def __init__(self, name, typenumber, node_parameters):

        # **********************
        # ***** Knotenname *****
        # **********************
        self.__name = name

        # **********************
        # ***** Knotentyp  *****
        # **********************
        # 0 = Slack-Knoten (Referenzknoten)
        # 1 = P-Q-Knoten (Lastknoten)
        # 2 = P-U-Knoten (Einspeisung)
        self.__grid_node_types_index = {1: "Slack-Knoten", 2: "P-Q-Knoten", 3: "P-U-Knoten"}
        self.__grid_node_types = {"slack": 1, "load": 2, "voltage": 3}
        self.__typenumber = typenumber

        # ***********************
        # **** Lastparameter ****
        # ***********************
        # Wirkleistung in kW
        self.__active_load_power = None
        # Blindleistung in kVar
        self.__reactive_load_power = None

        # ***********************
        # ***** Einspeisung *****
        # ***********************
        # Wirkleistung in kW
        self.__active_injection_power = None
        # Blindleistung in kVar
        self.__reactive_injection_power = None

        # ***************************
        # ***** Spannungswinkel *****
        # ***************************
        self.__theta = None

        # **************************
        # ***** Knotenspannung *****
        # **************************
        self.__node_voltage = None

        # Knotenparameter setzen
        self.set_node_parameters(node_parameters)

    # getter-Methoden
    def get_name(self):
        return self.__name

    def get_type_number(self):
        return self.__typenumber

    def get_grid_node_type_index_of(self, node_type):
        return self.__grid_node_types[node_type]

    # Methode gibt den Betrag der Spannungsggroeße zurück
    def get_node_voltage_magnitude(self):
        return self.__node_voltage

    # Methode gibt den Spannungswinkel in Bogenmaß zurück
    def get_node_voltage_angle(self):
        return self.__theta

    # Methode setzt die Knotenparameter in Abhaengigkeit des Knotentyps
    def set_node_parameters(self, node_parameters):

        # Fuer alle Knotentypen
        # ***********************
        # **** Lastparameter ****
        # ***********************
        # Wirkleistung in kW
        # Fuer alle Knotentypen (Last) Wirkleistung in kW
        self.__active_load_power = node_parameters[0]

        # Fuer alle Knotentypen (Last) Blindleistung in kVar
        self.__reactive_load_power = node_parameters[1]

        # Slack-Knoten (Referenzknoten)
        # setzen von: Knotenspannung (node_voltage) in kV, Spannungswinkel (theta) in Bogenmaß
        if self.__typenumber == self.get_grid_node_type_index_of("slack"):
            # Spannungsbetrag
            self.__node_voltage = node_parameters[5]
            self.__theta = node_parameters[4]

        # P-U-Knoten (Einspeisung)
        # setzen von : Wirkleistung in kW (active_injection_power), Knotenspannung (node_voltage) in kV
        elif self.__typenumber == self.get_grid_node_type_index_of("voltage"):
            self.__active_injection_power = node_parameters[2]
            self.__node_voltage = node_parameters[3]

        else:
            ERROR = ""

    # Bildschirmausgabe der Knotenparameter
    def __str__(self):
        result = ""
        result += "\n\n------------------------------------"
        result += "\nKnotenbezeichnung: " + str(self.__name)
        result += "\nKnotentyp: " + str(self.__grid_node_types_index[self.__typenumber])

        if self.__active_injection_power:
            result += "\n\nEinspeisung:"
            result += "\nWirkleistung P = " + str(self.__active_injection_power) + " kW"
            result += "\nBlindleistung Q = " + str(self.__reactive_injection_power) + " kVar"

        if self.__active_load_power:
            result += "\n\nLast:"
            result += "\nWirkleistung P = " + str(self.__active_load_power) + " kW"
            result += "\nBlindleistung Q = " + str(self.__reactive_load_power) + " kVar"

        if self.__node_voltage:
            result += "\n\nSpannung am Knoten: " + str(self.__node_voltage) + " kV"
            result += "\nSpannungswinkel: " + str(self.__theta) + "°"

        return result
