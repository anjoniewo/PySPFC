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
    def __init__(self, nodeNamei, nodeNamej, lineParameters, frequency):
        
        # Knoten 1
        self.nodeNamei = nodeNamei
        
        # Knoten 2
        self.nodeNamej = nodeNamej
        
        # Laenge der Leitung
        self.length
        
        # resistiver Laengswiderstand
        self.resistance
        
        # induktiver Laengswiderstand
        self.inductiveReactance

        # resistiver Querwiderstand
        self.transverseResistance
        
        # kapazitiver Querwiderstand
        self.capacitiveReactance
        
        # Laengsimpedanz der Leitung
        self.impedance
        
        # Laengsadmittanz der Leitung
        self.admittance
        
        # Querimpedanz der Leitung
        self.transverseImpedance
        
        # Queradmittanz der Leitung
        self.transverseAdmittance
        
        # Leitungsparameter setzen
        self.setLineParameters(lineParameters)
        
    # Methode setzt die Leitungsbelaege als Parameter
    def setLineParameters(self, lineParameters):
       
        # Leitungslaenge
        self.length = lineParameters[4]
       
        # resistiver Laengswiderstand
        self.resistance = lineParameters[0] * self.length

        # induktiver Laengswiderstand
        self.inductiveReactance = lineParameters[1] * self.length

        # resistiver Querwiderstand
        self.transverseResistance = lineParameters[2] * self.length

        # kapazitiver Querwiderstand
        self.capacitiveReactance = lineParameters[3] * self.length
        
        # Laengsimpedanz der Leitung
        self.impedance = Impedance(self.resistance, self.inductiveReactance)

        # Laengsadmittanz der Leitung
        self.admittance = Admittance(self.impedance)

        # Querimpedanz der Leitung
        self.transverseImpedance = Impedance(self.transverseResistance, self.capacitiveReactance)

        # Queradmittanz der Leitung
        self.transverseAdmittance = Admittance(self.transverseImpedance)

    # Bildschirmausgabe der Leitungsparameter
    def info(self):
        pprint(self)