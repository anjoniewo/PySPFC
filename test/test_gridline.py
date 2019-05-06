from unittest import TestCase
from main.grid.gridline import GridLine


# Klasse fuer GridLine-Tests
class TestGridLine(TestCase):

    # Methode fuer die Erstellung einer Liste mit GridLine-Parametern
    @staticmethod
    def test_create_line_parameters():
        gridline_parameters = list()
        gridline_parameters.append(0.2)
        gridline_parameters.append(0.05)
        gridline_parameters.append(0.01)
        gridline_parameters.append(1)
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
