import math
from loadflowreporter import LoadFlowReporter
from impedance import Impedance
from admittance import Admittance

# eine Leitung wird als Knotenverbindendes Netzelement definiert
class GridLine:

    # Initialisierungs-Konstruktor
    # node_i = Anfangsknoten
    # node_j = Endknoten
    # lineParameters: [0,1,2,3,4]
    # [0] -> [Leitungslaenge] = km
    # [1] -> [resistiver Längsleitungsbelag] = Ω/km
    # [2] -> [induktiver Längsleitungsbelag] = mH/km
    # [3] -> [resistiver Querleitungsbelag] = Ω/km
    # [4] -> [kapazitiver Querleitungsbelag] = nF/km
    def __init__(self, frequency, node_name_i, node_name_j, line_parameters):

        # Frequenz
        self.frequency = frequency

        # Knoten 1
        self.node_name_i = node_name_i

        # Knoten 2
        self.node_name_j = node_name_j

        # Laenge der Leitung
        self.length = None

        # resistiver Laengswiderstand
        self.resistance = None

        # induktiver Laengswiderstand
        self.inductive_reactance = None

        # resistiver Querwiderstand
        self.transverse_resistance = None
        
        # kapazitiver Querwiderstand
        self.capacitive_reactance = None

        # Laengsimpedanz der Leitung
        self.impedance = None
        
        # Laengsadmittanz der Leitung
        self.admittance = None
        
        # Querimpedanz der Leitung
        self.transverse_impedance = None
        
        # Queradmittanz der Leitung
        self.transverse_admittance = None

        # Queradmittanz der Leitung an einem Knoten,entspricht halben Queradmittanz-Wert der Leitung
        self.transverse_admittance_on_node = None

        # Leitungsparameter setzen
        self.set_line_parameters(line_parameters)

    # Methode setzt die Leitungsbelaege (Ω/km) als Parameter
    def set_line_parameters(self, line_parameters):
       
        # Leitungslaenge
        if line_parameters[0]:
            self.length = line_parameters[0]

            # resistiver Laengswiderstand
            if line_parameters[1] >= 0:
                self.resistance = line_parameters[1] * self.length

            # induktiver Laengswiderstand
            if line_parameters[2] > 0:
                self.inductive_reactance = (2 * math.pi * self.frequency * line_parameters[2]) * self.length

            # resistiver Querwiderstand
            if line_parameters[3] >= 0:
                self.transverse_resistance = line_parameters[3] * self.length

            # kapazitiver Querwiderstand
            if line_parameters[4] > 0:
                self.capacitive_reactance = (1 / (2 * math.pi * self.frequency * line_parameters[4])) * self.length

        else:
            LoadFlowReporter.error_report.append("Line-length: line_parameters[0] = 0")
            print(LoadFlowReporter.error_report)


        # Laengsimpedanz der Leitung
        if self.resistance or self.inductive_reactance:
            self.impedance = Impedance(self.resistance, self.inductive_reactance)

        # Laengsadmittanz der Leitung
        if self.impedance is not None:
            self.admittance = Admittance(self.impedance)

        # Querimpedanz der Leitung
        if self.transverse_resistance or self.capacitive_reactance:
            self.transverse_impedance = Impedance(self.transverse_resistance, self.capacitive_reactance)

        # Queradmittanz der Leitung
        if self.transverse_impedance is not None:
            self.transverse_admittance = Admittance(self.transverse_impedance)

        # Knoten-Queradmittanz der Leitung bezogen auf einen Knoten, entspricht halben Queradmittanz-Wert
        if self.transverse_admittance is not None:
            self.transverse_admittance_on_node = self.transverse_admittance
            self.transverse_admittance_on_node.g /= 2
            self.transverse_admittance_on_node.b /= 2

    # Bildschirmausgabe der Leitungsparameter
    def info(self):
        print("\n----------------------------------")
        print("LEITUNG/KABEL")
        print("Knoten 1: " + str(self.node_name_i))
        print("Knoten 2: " + str(self.node_name_j))
        print("Länge: " + str(self.length) + " km " + "--> " + str(self.length * 1000) + " m")
        print("Längswiderstand: " + str(self.resistance) + " Ω")
        print("induktiver Längswiderstand: " + str(self.inductive_reactance) + " Ω")
        print("Querwiderstand: " + str(self.transverse_resistance))
        print("kapazitiver Querwiderstand: " + str(self.capacitive_reactance) + " Ω")
        print("Impedanz: " + str(self.impedance.get_magnitude()) + " Ω")
        print("Admittanz: " + str(self.admittance.get_magnitude()) + " S")
        print("Quer-Impedanz: " + str(self.transverse_impedance) + " Ω")
        print("Quer-Admittanz: " + str(self.transverse_admittance) + " S")
