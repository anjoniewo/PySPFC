from unittest import TestCase

from simplepowerflow.powerflow.griddataimport.csvparser import CSVParser


class TestCSVParser(TestCase):
    def test_import_csv_files(self):
        csv_parser = CSVParser()