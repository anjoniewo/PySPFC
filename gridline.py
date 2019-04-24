import math
from impedance import Impedance
from admittance import Admittance

# eine Leitung wird als Knotenverbindendes Netzelement definiert
class GridLine:

    # Initialisierungs-Konstruktor
    # node_i = Anfangsknoten
    # node_j = Endknoten
    # lineParameters: (BISLANG!!!!)
    # r_len_L = resistiver Leitungsbelag (Ω/km)
    # x_len_L = induktiver Leitungsbelag (Ω/km)
    # r_quer_L = resistiver Querleitungsbelag (Ω/km)
    # x_quer_L = kapazitiver Querleitungsbelag (Ω/km)
    # length = Leitungslaenge (km)
    def __init__(self, node_name_i, node_name_j, line_parameters):
        
        # Knoten 1
        self.node_name_i = node_name_i
        
        # Knoten 2
        self.node_name_j = node_name_j
        
        # Laenge der Leitung
        self.length
        
        # resistiver Laengswiderstand
        self.resistance
        
        # induktiver Laengswiderstand
        self.inductive_reactance

        # resistiver Querwiderstand
        self.transverse_resistance
        
        # kapazitiver Querwiderstand
        self.capacitive_reactance
        
        # Laengsimpedanz der Leitung
        self.impedance
        
        # Laengsadmittanz der Leitung
        self.admittance
        
        # Querimpedanz der Leitung
        self.transverse_impedance
        
        # Queradmittanz der Leitung
        self.transverse_admittance
        
        # Leitungsparameter setzen
        self.set_line_parameters(line_parameters)
        
    # Methode setzt die Leitungsbelaege als Parameter
    def set_line_parameters(self, line_parameters):
       
        # Leitungslaenge
        self.length = line_parameters[4]
       
        # resistiver Laengswiderstand
        self.resistance = line_parameters[0] * self.length

        # induktiver Laengswiderstand
        self.inductive_reactance = line_parameters[1] * self.length

        # resistiver Querwiderstand
        self.transverse_resistance = line_parameters[2] * self.length

        # kapazitiver Querwiderstand
        self.capacitive_reactance = line_parameters[3] * self.length
        
        # Laengsimpedanz der Leitung
        self.impedance = Impedance(self.resistance, self.inductive_reactance)

        # Laengsadmittanz der Leitung
        self.admittance = Admittance(self.impedance)

        # Querimpedanz der Leitung
        self.transverse_impedance = Impedance(self.transverse_resistance, self.capacitive_reactance)

        # Queradmittanz der Leitung
        self.transverse_admittance = Admittance(self.transverse_impedance)

    # Bildschirmausgabe der Leitungsparameter
    def info(self):
        print("")
        print("----------------------------------")
        print("Leitung")
        print("Knoten 1: " + str(self.node_name_i))
        print("Knoten 2: " + str(self.node_name_j))