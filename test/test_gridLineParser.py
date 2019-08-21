import os
from unittest import TestCase

from simplepowerflow import GridLineParser


class TestGridLineParser(TestCase):

    def test_gridline_parser(self):
        # Erstelle Dateipfad zu grideline- und gridnode-Dateien
        csv_files_path = os.path.join(os.path.dirname(__file__), "test_files/7_knoten_mit_trafo")

        # Dateipfad fuer gridline-Datei
        gridline_path = os.path.join(csv_files_path, "lines.csv")

        grid_line_parser = GridLineParser(file_path=gridline_path)
