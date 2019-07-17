class Generator:
	
	def __init__(self, name, node_i, p_series, q_series, p_min=0, p_max=0, q_min=0, q_max=0):
		self.__name = name
		self.__node_i = node_i
		self.__p_series = p_series
		self.__q_series = q_series
		self.__p_min = p_min
		self.__p_max = p_max
		self.__q_min = q_min
		self.__q_max = q_max
