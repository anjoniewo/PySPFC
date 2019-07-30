from simplepowerflow.powerflow.griddataimport.ALT_gridlineparser import GridLineParser
from simplepowerflow.powerflow.griddataimport.ALT_gridnodeparser import GridNodeParser
from simplepowerflow.powerflow.griddataimport.ALT_transformerparser import TransformerParser


class GridImport:

    def __init__(self, gridline_file_path="", gridnode_file_path="", transformer_path=""):
        self.__grid_line_parser = GridLineParser(gridline_file_path)
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
