from LoadFlowTool.loadflowtool.griddataimport.csvparser import CSVParser
from LoadFlowTool.loadflowtool.grid.gridline import GridLine


# Parser-Klasse zum Einlesen der Leitungsdaten
class GridLineParser(CSVParser):

    def __init__(self, file_path, frequency):

        super(GridLineParser, self).__init__()

        self.__gridlines = list()

        self.__read_line_parameters(file_path)
        self.__get_lines_from_csv_dictionary(frequency)

    # getter
    def get_gridlines(self):
        return self.__gridlines

    def __read_line_parameters(self, file_path):
        self.read_csv_to_dictionary(file_path)

    def __get_lines_from_csv_dictionary(self, frequency):

        parameter_list = list()

        list_of_keys = list(self.csv_dictionary.keys())

        # wenn das csv dictionary nicht leer ist
        if list_of_keys:
            number_of_gridnodes = len(self.csv_dictionary[list_of_keys[0]])

            # alle Eintraege des dictionaries durchgehen
            for i in range(number_of_gridnodes):
                for key in self.csv_dictionary:
                    if key == "name":
                        name = self.csv_dictionary[key][i]
                    elif key == "node_i":
                        node_i = self.csv_dictionary[key][i]
                    elif key == "node_j":
                        node_j = self.csv_dictionary[key][i]
                    elif key == "length in km":
                        parameter_list.append(float(self.csv_dictionary[key][i]))
                    elif key == "r":
                        parameter_list.append(float(self.csv_dictionary[key][i]))
                    elif key == "x":
                        parameter_list.append(float(self.csv_dictionary[key][i]))
                    elif key == "g_shunt":
                        parameter_list.append(
                            None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))
                    elif key == "b_shunt":
                        parameter_list.append(
                            None if not self.csv_dictionary[key][i] else float(self.csv_dictionary[key][i]))

                gridline = GridLine(frequency, name, node_i, node_j, parameter_list)
                self.__gridlines.append(gridline)
                parameter_list = list()
