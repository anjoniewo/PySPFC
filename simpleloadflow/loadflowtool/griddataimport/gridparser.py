from simpleloadflow.loadflowtool.griddataimport.gridlineparser import GridLineParser
from simpleloadflow.loadflowtool.griddataimport.gridnodeparser import GridNodeParser
from simpleloadflow.loadflowtool.griddataimport.transformerparser import TransformerParser


class GridParser:

    def __init__(self, frequency, gridline_file_path="", gridnode_file_path="", transformer_path=""):
        self.grid_line_parser = GridLineParser(gridline_file_path, frequency)
        self.grid_node_parser = GridNodeParser(gridnode_file_path)
        self.transformer_parser = TransformerParser(transformer_path)
