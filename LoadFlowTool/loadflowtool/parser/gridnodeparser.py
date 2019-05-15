# Parser-Klasse zum Einleser der Leitungsdaten
from LoadFlowTool.loadflowtool.parser.csvparser import CSVParser
from LoadFlowTool.loadflowtool.grid.gridnode import GridNode


class GridNodeParser(CSVParser):

    def __init__(self, file_path):

        super(GridNodeParser, self).__init__()

        self.__gridnodes = list()

        self.__read_node_parameters(file_path)
        self.__get_nodes_from_csv_dictionary()

    # getter
    def get_gridnodes(self):
        return self.__gridnodes

    def __read_node_parameters(self, file_path):
        self.read_csv_to_dictionary(file_path)

    def __get_nodes_from_csv_dictionary(self):

        list_of_keys = list(self.csv_dictionary.keys())

        # wenn das csv dictionary nicht leer ist
        if list_of_keys:
            number_of_gridnodes = len(self.csv_dictionary[list_of_keys[0]])

            # alle Eintraege des dictionaries durchgehen
            for i in range(0, number_of_gridnodes):
                parameter_list = list()
                for key in self.csv_dictionary:
                    if key == "name":
                        gridnode_name = self.csv_dictionary[key][i]
                    elif key == "typenumber":
                        type_number = int(self.csv_dictionary[key][i])
                    elif key == "active_load_power":
                        parameter_list.append(self.csv_dictionary[key][i])
                    elif key == "reactive_load_power":
                        parameter_list.append(self.csv_dictionary[key][i])
                    elif key == "active_injection_power":
                        parameter_list.append(self.csv_dictionary[key][i])
                    elif key == "reactive_injection_power":
                        parameter_list.append(self.csv_dictionary[key][i])
                    elif key == "theta in rad":
                        parameter_list.append(self.csv_dictionary[key][i])
                    elif key == "node_voltage in kV":
                        parameter_list.append(self.csv_dictionary[key][i])

                gridnode = GridNode(gridnode_name, type_number,
                                    self.__get_node_parameters_by_type(type_number, parameter_list))
                self.__gridnodes.append(gridnode)

    def __get_node_parameters_by_type(self, type_number, list_of_parameters):

        grid_node_parameters = list()

        active_load_power = float(list_of_parameters[0]) if list_of_parameters[0] else None
        reactive_load_power = float(list_of_parameters[1]) if list_of_parameters[1] else None
        grid_node_parameters.append(active_load_power)
        grid_node_parameters.append(reactive_load_power)

        if type_number == 0:
            node_voltage = float(list_of_parameters[5]) if list_of_parameters[5] else None
            grid_node_parameters.append(node_voltage)

            theta = float(list_of_parameters[4]) if list_of_parameters[4] else None
            grid_node_parameters.append(theta)
        elif type_number == 2:
            active_injection_power = float(list_of_parameters[2]) if list_of_parameters[2] else None
            grid_node_parameters.append(active_injection_power)

            node_voltage = float(list_of_parameters[5]) if list_of_parameters[5] else None
            grid_node_parameters.append(node_voltage)

        return grid_node_parameters
