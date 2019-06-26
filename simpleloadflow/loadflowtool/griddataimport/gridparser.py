from simpleloadflow.loadflowtool.griddataimport.gridlineparser import GridLineParser
from simpleloadflow.loadflowtool.griddataimport.gridnodeparser import GridNodeParser
from simpleloadflow.loadflowtool.griddataimport.transformerparser import TransformerParser


class GridParser:

    def __init__(self, frequency, gridline_file_path="", gridnode_file_path="", transformer_path=""):
        self.__grid_line_parser = GridLineParser(gridline_file_path, frequency)
        self.__grid_node_parser = GridNodeParser(gridnode_file_path)
        self.__transformer_parser = TransformerParser(transformer_path)

    def __get_gridlines(self):
        return self.__grid_line_parser.get_gridlines()

    def __get_gridnodes(self):
        return self.__grid_node_parser.get_gridnodes()

    def __get_transformers(self):
        return self.__transformer_parser.get_transformers()

    gridlines = property(__get_gridlines)
    gridnodes = property(__get_gridnodes)
    transformers = property(__get_transformers)
