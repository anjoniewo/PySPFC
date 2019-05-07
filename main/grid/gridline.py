import math
from main.loadflowreporter import LoadFlowReporter
from main.impedance import Impedance
from main.admittance import Admittance


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
		self.__frequency = frequency
		
		# Knoten 1
		self.__node_name_i = node_name_i
		
		# Knoten 2
		self.__node_name_j = node_name_j
		
		# Laenge der Leitung
		self.__length = None
		
		# resistiver Laengswiderstand
		self.__resistance = None
		
		# induktiver Laengswiderstand
		self.__inductive_reactance = None
		
		# resistiver Querwiderstand
		self.__transverse_resistance = None
		
		# kapazitiver Querwiderstand
		self.__capacitive_reactance = None
		
		# Laengsimpedanz der Leitung
		self.__impedance = None
		
		# Laengsadmittanz der Leitung
		self.__admittance = None
		
		# Querimpedanz der Leitung
		self.__transverse_impedance = None
		
		# Queradmittanz der Leitung
		self.__transverse_admittance = None
		
		# Queradmittanz der Leitung an einem Knoten,entspricht halben Queradmittanz-Wert der Leitung
		self.__transverse_admittance_on_node = None
		
		# Leitungsparameter setzen
		self.__set_line_parameters(line_parameters)
	
	# getter-Methoden
	def get_node_name_i(self):
		return self.__node_name_i
	
	def get_node_name_j(self):
		return self.__node_name_j
	
	def get_admittance(self):
		return self.__admittance
	
	def get_frequency(self):
		return self.__freqeuncy
	
	def get_transverse_admittance_on_node(self):
		return self.__transverse_admittance_on_node
	
	# Methode setzt die Leitungsbelaege (Ω/km) als Parameter
	def __set_line_parameters(self, line_parameters):
		
		# Leitungslaenge
		if line_parameters[0]:
			self.__length = line_parameters[0]
			
			# resistiver Laengswiderstand
			if line_parameters[1] >= 0:
				self.__resistance = line_parameters[1] * self.__length
			
			# induktiver Laengswiderstand
			if line_parameters[2] > 0:
				self.__inductive_reactance = (2 * math.pi * self.__frequency * line_parameters[2]) * self.__length
			
			# resistiver Querwiderstand
			if line_parameters[3] >= 0:
				self.__transverse_resistance = line_parameters[3] * self.__length
			
			# kapazitiver Querwiderstand
			if line_parameters[4] > 0:
				self.__capacitive_reactance = (1 / (
						2 * math.pi * self.__frequency * line_parameters[4])) * self.__length
		
		else:
			LoadFlowReporter.error_report.append("Line-length: line_parameters[0] = 0")
			print(LoadFlowReporter.error_report)
		
		# Laengsimpedanz der Leitung
		if self.__resistance or self.__inductive_reactance:
			self.__impedance = Impedance(self.__resistance, self.__inductive_reactance)
		
		# Laengsadmittanz der Leitung
		if self.__impedance is not None:
			self.__admittance = Admittance(self.__impedance)
		
		# Querimpedanz der Leitung
		if self.__transverse_resistance or self.__capacitive_reactance:
			self.__transverse_impedance = Impedance(self.__transverse_resistance, self.__capacitive_reactance)
		
		# Queradmittanz der Leitung
		if self.__transverse_impedance is not None:
			self.__transverse_admittance = Admittance(self.__transverse_impedance)
		
		# Knoten-Queradmittanz der Leitung bezogen auf einen Knoten, entspricht halben Queradmittanz-Wert
		if self.__transverse_admittance is not None:
			self.__transverse_admittance_on_node = Admittance(g=self.__transverse_admittance.get_real_part() / 2,
			                                                  b=self.__transverse_admittance.get_imaginary_part() / 2)
	
	# Bildschirmausgabe der Leitungsparameter
	def info(self):
		print("\n----------------------------------")
		print("LEITUNG/KABEL")
		print("Knoten 1: " + str(self.__node_name_i))
		print("Knoten 2: " + str(self.__node_name_j))
		print("Länge: " + str(self.__length) + " km " + "--> " + str(self.__length * 1000) + " m")
		print("Längswiderstand: " + str(self.__resistance) + " Ω")
		print("induktiver Längswiderstand: " + str(self.__inductive_reactance) + " Ω")
		print("Querwiderstand: " + str(self.__transverse_resistance))
		print("kapazitiver Querwiderstand: " + str(self.__capacitive_reactance) + " Ω")
		print("Impedanz: " + str(self.__impedance.get_magnitude()) + " Ω")
		print("Admittanz: " + str(self.__admittance.get_magnitude()) + " S")
		print("Quer-Impedanz: " + str(self.__transverse_impedance) + " Ω")
		print("Quer-Admittanz: " + str(self.__transverse_admittance) + " S")
