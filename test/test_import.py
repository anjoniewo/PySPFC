from unittest import TestCase

from simplepowerflow.powerflow.griddataimport.csvimport import *


class TestImport(TestCase):
    def test_import_csv_files(self):
        csv_import = CSVimport()
        csv_import.import_csv_files()