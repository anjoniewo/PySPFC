from simplepowerflow.powerflow.grid.generator import Generator


class Load(Generator):
	"""
		class to model loads connected to a grid node
	"""
	
	def __init__(self, name, node_i):
		self.__name = name
		self.__node_i = node_i
		self.__p_q_series = None
	
	def __get_name(self):
		return self.__name
	
	def __get_node_name(self):
		return self.__node_i
	
	name = property(__get_name)
	node = property(__get_node_name)
	
	def set_p_q_series(self, p_q_series):
		self.__p_q_series = p_q_series
