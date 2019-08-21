from simplepowerflow.gridelements.admittance import Admittance
from simplepowerflow.gridelements.impedance import Impedance
from simplepowerflow.powerflow.powerflowreporter import LoadFlowReporter


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
	def __init__(self, name, node_name_i, node_name_j, line_parameters):
		
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
	def __get_name(self):
		return self.__name
	
	def get_node_name_i(self):
		return self.__node_name_i
	
	def get_node_name_j(self):
		return self.__node_name_j
	
	def get_admittance(self):
		return self.__admittance
	
	def get_transverse_admittance_on_node(self):
		return self.__transverse_admittance_on_node
	
	name = property(__get_name)
	
	# node_i = property(__get_node_name_i)
	# node_j = property(__get_node_name_j)
	# admittance = property(__get_admittance)
	# shunt_admittance = property(__get_transverse_admittance_on_node)
	
	def set_admittance(self, real_part, imag_part):
		self.__admittance = Admittance(g=real_part, b=imag_part)
	
	def set_transverse_admittance(self, real_part, imag_part):
		self.__transverse_admittance = Admittance(g=real_part, b=imag_part)
	
	# Methode setzt die Leitungsbelaege (Ω/km) als Parameter
	def __set_line_parameters(self, line_parameters):
		
		if line_parameters:
			
			# Leitungslaenge
			self.__length = line_parameters['length']
			
			# resistiver Laengswiderstand
			self.__resistance = line_parameters['r_l'] * self.__length
			
			# induktiver Laengswiderstand
			self.__inductive_reactance = line_parameters['x_l'] * self.__length
			
			# resistiver Querwiderstand
			self.__transverse_resistance = line_parameters['g_shunt_l'] * self.__length
			
			# kapazitiver Querwiderstand
			self.__capacitive_reactance = line_parameters['b_shunt_l'] * self.__length
		
		else:
			LoadFlowReporter.error_report.append("Coudn't read line_parameters.")
			print(LoadFlowReporter.error_report)
		
		# Laengsimpedanz der Leitung
		if self.__resistance or self.__inductive_reactance:
			self.__impedance = Impedance(self.__resistance, self.__inductive_reactance)
		
		# Laengsadmittanz der Leitung
		if self.__impedance is not None:
			self.__admittance = Admittance(impedance=self.__impedance)
		
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
