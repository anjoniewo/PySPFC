from simplepowerflow.powerflow.grid.generator import Generator


class Load(Generator):
    """
        class to model loads connected to a grid node
    """

    def __init__(self, name, node_i, p_q_series, p_min=0, p_max=0,
                 q_min=0, q_max=0):
        self.__name = name
        self.__node_i = node_i
        self.__p_q_series = p_q_series
        self.__p_min = p_min
        self.__p_max = p_max
        self.__q_min = q_min
        self.__q_max = q_max
