class Generator:
    """
        class to model generators connected to a gridelements node
    """

    def __init__(self, name, node_i, p_min=100, p_max=100, q_min=100, q_max=100):
        self.__name = name
        self.__node_i = node_i
        self.__p_q_series = None
        self.__p_min = p_min
        self.__p_max = p_max
        self.__q_min = q_min
        self.__q_max = q_max

    def __get_name(self):
        return self.__name

    def __get_node_name(self):
        return self.__node_i

    def __get_p_max(self):
        return self.__p_max

    def __get_p_min(self):
        return self.__p_min

    def __get_q_max(self):
        return self.__q_max

    def __get_q_min(self):
        return self.__q_min

    def __get_series_data(self):
        return self.__p_q_series

    name = property(__get_name)
    node = property(__get_node_name)
    p_max = property(__get_p_max)
    p_min = property(__get_p_min)
    q_max = property(__get_q_max)
    q_min = property(__get_q_min)
    series_data = property(__get_series_data)

    def set_p_q_series(self, p_q_series):
        self.__p_q_series = p_q_series
