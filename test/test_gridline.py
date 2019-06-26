from unittest import TestCase
from simplepowerflow.powerflowtool.grid.gridline import GridLine


# Klasse fuer GridLine-Tests
class TestGridLine(TestCase):

    # Methode fuer die Erstellung einer Liste mit GridLine-Parametern
    @staticmethod
    def test_create_line_parameters(length, r, xl, r_quer, xc_quer):
        gridline_parameters = list()
        # Länge
        gridline_parameters.append(length)
        # resistiver Längswiderstand
        gridline_parameters.append(r)
        # induktiver Längswiderstand
        gridline_parameters.append(xl)
        # resitiver Querwiderstand
        gridline_parameters.append(r_quer)
        # kapazitiver Querwiderstand
        gridline_parameters.append(xc_quer)

        return gridline_parameters

    # Test fuer die Instanzierung eines GridLine-Objekts
    def test_set_line_parameters(self):
        branch_1 = GridLine(50, "K0", "K1", self.test_create_line_parameters(1, 1, 1, 1, 1))
        assert branch_1.get_frequency(), 50

    # Test fuer die Konsolenausgabe der Parameter eines GridLine-Objektes
    def test_info(self):
        branch_1 = GridLine(50, "K0", "K1", self.test_create_line_parameters(1, 1, 1, 1, 1))
        branch_1.info()
        assert branch_1.node_name_i, "K1"
