from simplepowerflow.gridelements.generator import Generator


class Load(Generator):
	"""
		class to model loads connected to a gridelements node
	"""
	
	def __init__(self, name, node_i):
		self.__name = name
		self.__node_i = node_i
		self.__p_q_series = None
	
	def __get_name(self):
		return self.__name
	
	def __get_node_name(self):
		return self.__node_i

	def __get_series_data(self):
		return self.__p_q_series
	
	name = property(__get_name)
	node = property(__get_node_name)
	series_data = property(__get_series_data)
	
	def set_p_q_series(self, p_q_series):
		self.__p_q_series = p_q_series
