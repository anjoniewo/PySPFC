from LoadFlowTool.loadflowtool.loadflow.loadflowreporter import LoadFlowReporter
from LoadFlowTool.loadflowtool.grid.impedance import Impedance
from LoadFlowTool.loadflowtool.grid.admittance import Admittance


# eine Leitung wird als Knotenverbindendes Netzelement definiert
class GridLine:
	
	# Initialisierungs-Konstruktor
	# name = Leitungsbezeichnung
	# node_i = Anfangsknoten
	# node_j = Endknoten
	# lineParameters: [0,1,2,3,4]
	# [0] -> [Leitungslaenge] = km
	# [1] -> r [resistiver Längswiderstand] = Ω
	# [2] -> x [induktiver Längswiderstand] = Ω
	# [3] -> g [resistiver Querleitungswiderstand] = 1/Ω
	# [4] -> b [kapazitiver Querleitungwert] = 1/Ω
	def __init__(self, frequency, name, node_name_i, node_name_j, line_parameters):
		
		# Frequenz
		self.__frequency = frequency
		
		# Leitungsbezeichnung
		self.__name = name
		
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
	def get_name(self):
		return self.__name
	
	def get_node_name_i(self):
		return self.__node_name_i
	
	def get_node_name_j(self):
		return self.__node_name_j
	
	def get_admittance(self):
		return self.__admittance
	
	def get_frequency(self):
		return self.__frequency
	
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
			if line_parameters[2] >= 0:
				# self.__inductive_reactance = (2 * math.pi * self.__frequency * line_parameters[2]) * self.__length
				# induktiver Belag * Leitungslaenge
				self.__inductive_reactance = line_parameters[2] * self.__length
			
			# resistiver Querwiderstand
			if line_parameters[3]:
				self.__transverse_resistance = line_parameters[3] * self.__length
			
			# kapazitiver Querwiderstand
			if line_parameters[4]:
				# self.__capacitive_reactance = (1 / (
				# 		2 * math.pi * self.__frequency * line_parameters[4])) * self.__length
				self.__capacitive_reactance = line_parameters[4] * self.__length
		
		else:
			LoadFlowReporter.error_report.append("Line-length: line_parameters[0] = 0")
			print(LoadFlowReporter.error_report)
		
		# Laengsimpedanz der Leitung
		if self.__resistance or self.__inductive_reactance:
			self.__impedance = Impedance(self.__resistance, self.__inductive_reactance)
		
		# Laengsadmittanz der Leitung
		if self.__impedance is not None:
			self.__admittance = Admittance(impedance=self.__impedance)
		
		# # Querimpedanz der Leitung
		# if self.__transverse_resistance or self.__capacitive_reactance:
		#     self.__transverse_impedance = Impedance(self.__transverse_resistance, self.__capacitive_reactance,
		#                                             in_series=False)
		
		# Queradmittanz der Leitung
		# if self.__transverse_impedance is not None:
		self.__transverse_admittance = Admittance(g=self.__transverse_resistance, b=self.__capacitive_reactance)
		
		# Knoten-Queradmittanz der Leitung bezogen auf einen Knoten, entspricht halben Queradmittanz-Wert
		if self.__transverse_admittance is not None:
			self.__transverse_admittance_on_node = Admittance(
				g=((
						   self.__transverse_admittance.get_real_part() / 2) if self.__transverse_admittance.get_real_part() else None),
				b=((
						self.__transverse_admittance.get_imaginary_part() / 2)) if self.__transverse_admittance.get_imaginary_part() else None)
	
	# Bildschirmausgabe der Leitungsparameter
	def __str__(self):
		result = ""
		result += "\n\n----------------------------------"
		result += "\nLEITUNG/KABEL"
		result += "\nLeitungsbezeichnung: " + str(self.__name)
		result += "\nKnoten 1: " + str(self.__node_name_i)
		result += "\nKnoten 2: " + str(self.__node_name_j)
		result += "\nLänge: " + str(self.__length) + " km " + "--> " + str(self.__length * 1000) + " m"
		result += "\nLängswiderstand: " + str(self.__resistance) + " Ω"
		result += "\ninduktiver Längswiderstand: " + str(self.__inductive_reactance) + " Ω"
		result += "\nQuerwiderstand: " + str(self.__transverse_resistance)
		result += "\nkapazitiver Querwiderstand: " + str(self.__capacitive_reactance) + " Ω"
		result += "\nImpedanz: " + str(self.__impedance.get_magnitude()) + " Ω"
		result += "\nAdmittanz: " + str(self.__admittance.get_magnitude()) + " S"
		result += "\nQuer-Impedanz: " + str(self.__transverse_impedance) + " Ω"
		result += "\nQuer-Admittanz: " + str(self.__transverse_admittance) + " S"
		
		return result
