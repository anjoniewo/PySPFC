from unittest import TestCase
from LoadFlowTool.loadflowtool.grid.gridline import GridLine


# Klasse fuer GridLine-Tests
class TestGridLine(TestCase):

    # Methode fuer die Erstellung einer Liste mit GridLine-Parametern
    @staticmethod
    def test_create_line_parameters():
        gridline_parameters = list()
        # Länge
        gridline_parameters.append(1)
        # resistiver Längswiderstand
        gridline_parameters.append(1)
        # induktiver Längswiderstand
        gridline_parameters.append(1)
        # resitiver Querwiderstand
        gridline_parameters.append(1)
        # kapazitiver Querwiderstand
        gridline_parameters.append(1)

        return gridline_parameters

    # Test fuer die Instanzierung eines GridLine-Objekts
    def test_set_line_parameters(self):
        branch_1 = GridLine(50, "K0", "K1", self.test_create_line_parameters())
        assert (branch_1.get_frequency(), 50)

    # Test fuer die Konsolenausgabe der Parameter eines GridLine-Objektes
    def test_info(self):
        branch_1 = GridLine(50, "K0", "K1", self.test_create_line_parameters())
        branch_1.info()
        assert (branch_1.node_name_i, "K1")
