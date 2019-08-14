from unittest import TestCase

from simplepowerflow.simplepowerflow.griddataimport.ALT_csvparser import CSVParser


class TestCSVParser(TestCase):
    def test_import_csv_files(self):
        csv_parser = CSVParser()
