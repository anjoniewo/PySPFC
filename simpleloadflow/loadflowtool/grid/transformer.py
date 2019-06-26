from simpleloadflow.loadflowtool.loadflow.loadflowreporter import LoadFlowReporter
from simpleloadflow.loadflowtool.grid.impedance import Impedance
from simpleloadflow.loadflowtool.grid.admittance import Admittance


# ein Transformator wird als Knotenverbindendes Netzelement definiert
class Transformer:
	
	# Initialisierungs-Konstruktor
	# name = Trafoname
	# node_i = Anfangsknoten
	# node_j = Endknoten
	# transformer_parameters: [0,1,2,3,4]
	def __init__(self, name, node_name_i, node_name_j, transformer_parameters):
		
		# Transformatorbezeichnung
		self.__name = name
		
		# Knoten 1
		self.__node_name_i = node_name_i
		
		# Knoten 2
		self.__node_name_j = node_name_j
		
		# resistiver Laengswiderstand der Kurzschlussimpedanz
		self.__r = None
		
		# induktiver Laengswiderstand der Kurzschlussimpedanz
		self.__x = None
		
		# Kurzschlussimpedanz des Transformators
		self.__sc_impedance = None
		
		# Kurzschlussadmittanz des Transformators
		self._sc_admittance = None
		
		# Konduktanz der Shunt-Admittanz
		self.__g = None
		
		# Suszeptanz der Shunt-Admittanz
		self.__b = None
		
		# Shunt-Impedanz des Transformators
		self.__shunt_impedance = None
		
		# Shunt-Admittanz des Transformators
		self.__shunt_admittance = None
		
		# Stufenstellung
		self.__tap_ratio = None
		
		# Phasenwinkel falls Regeltrafo
		self.__phase_shift = None
		
		# Nennscheinleistungsgrenze
		self.__s_n = None
		
		self.__set_transformer_parameters(transformer_parameters)
	
	# getter-Methoden
	def get_name(self):
		return self.__name
	
	def get_node_name_i(self):
		return self.__node_name_i
	
	def get_node_name_j(self):
		return self.__node_name_j
	
	def get_sc_admittance(self):
		return self.__sc_admittance
	
	# Methode setzt die Transformatordaten
	def __set_transformer_parameters(self, transformer_parameters):
		
		# resistiver Laengswiderstand der Kurzschlussimpedanz
		if transformer_parameters[0]:
			self.__r = transformer_parameters[0]
		
		if transformer_parameters[1]:
			self.__x = transformer_parameters[1]
		
		if transformer_parameters[2]:
			self.__g = transformer_parameters[2]
		
		if transformer_parameters[3]:
			self.__b = transformer_parameters[3]
		
		if transformer_parameters[4]:
			self.__tap_ratio = transformer_parameters[4]
		
		if transformer_parameters[5]:
			self.__phase_shift = transformer_parameters[5]
		
		if transformer_parameters[6]:
			self.__s_n = transformer_parameters[6]
		
		else:
			LoadFlowReporter.error_report.append("Transformer ERROR")
			print(LoadFlowReporter.error_report)
		
		# Kurzschlussimpedanz des Transformators
		if self.__r and self.__x:
			self.__sc_impedance = Impedance(self.__r, self.__x)
		
		# Kurzschlussadmittanz des Transformators
		if self.__sc_impedance is not None:
			self.__sc_admittance = Admittance(impedance=self.__sc_impedance)
		
		# Shunt-Admittanz des Transformators
		if self.__g and self.__b:
			self.__shunt_admittance = Admittance(g=self.__g, b=self.__b)
		
		# Shunt-Impedanz des Transformators
		if self.__shunt_admittance is not None:
			self.__shunt_impedance = Impedance(admittance=self.__shunt_admittance)
