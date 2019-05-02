from loadflowreporter import LoadFlowReporter

# ein Knoten ist ein Netzelement an einem bestimmten Punkt im Netz
class GridNode:

    # Initialisierungs-Konstruktor
    def __init__(self, name, typenumber, node_parameters):

        # **********************
        # ***** Knotenname *****
        # **********************
        self.name = name

        # **********************
        # ***** Knotentyp  *****
        # **********************
        # 0 = Slack-Knoten (Referenzknoten)
        # 1 = P-Q-Knoten (Lastknoten)
        # 2 = P-U-Knoten (Einspeisung)
        self.grid_node_types = {0: "Slack-Knoten", 1: "P-Q-Knoten", 2: "P-U-Knoten"}
        self.typenumber = typenumber

        # ***********************
        # **** Lastparameter ****
        # ***********************
        # Wirkleistung in kW
        self.active_load_power = None
        # Blindleistung in kVar
        self.reactive_load_power = None

        # ***********************
        # ***** Einspeisung *****
        # ***********************
        # Wirkleistung in kW
        self.active_injection_power = None
        # Blindleistung in kVar
        self.reactive_injection_power = None

        # ***************************
        # ***** Spannungswinkel *****
        # ***************************
        self.theta = None

        # **************************
        # ***** Knotenspannung *****
        # **************************
        self.node_voltage = None
        
        # Knotenparameter setzen
        self.set_node_parameters(node_parameters)

    # Methode setzt die Knotenparameter in Abhaengigkeit des Knotentyps
    def set_node_parameters(self, node_parameters):
    
        # Fuer alle Knotentypen
        # ***********************
        # **** Lastparameter ****
        # ***********************
        # Wirkleistung in kW
        # Fuer alle Knotentypen (Last) Wirkleistung in kW
        self.active_load_power = node_parameters[0]

        # Fuer alle Knotentypen (Last) Blindleistung in kVar
        self.reactive_load_power = node_parameters[1]
        
        # Slack-Knoten (Referenzknoten)
        # setzen von: Knotenspannung (node_voltage) in kV, Spannungswinkel (theta) in Bogenmaß
        if self.typenumber == 0:
            # Spannungsbetrag
            self.node_voltage = node_parameters[2]
            self.theta = node_parameters[3]

        # P-U-Knoten (Einspeisung)
        # setzen von : Wirkleistung in kW (active_injection_power), Knotenspannung (node_voltage) in kV
        elif self.typenumber == 2:
            self.active_injection_power = node_parameters[2]
            self.node_voltage = node_parameters[3]

        else:
            ERROR = ""

    # Bildschirmausgabe der Knotenparameter
    def info(self):
        print("\n------------------------------------")
        print("Knotenbezeichnung: " + str(self.name))
        print("Knotentyp: " + str(self.grid_node_types[self.typenumber]))

        if self.active_injection_power:
            print("\nEinspeisung:")
            print("Wirkleistung P = " + str(self.active_injection_power) + " kW")
            print("Blindleistung Q = " + str(self.reactive_injection_power) + " kVar")
            
        if self.active_load_power:
            print("\nLast:")
            print("Wirkleistung P = " + str(self.active_load_power) + " kW")
            print("Blindleistung Q = " + str(self.reactive_load_power) + " kVar")

        if self.node_voltage:
            print("\nSpannung am Knoten: " + str(self.node_voltage))
            print("Spannungswinkel: " + str(self.theta))
