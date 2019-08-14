from unittest import TestCase

from simplepowerflow.simplepowerflow.csvimport import *


class TestImport(TestCase):
    def test_import_csv_files(self):
        csv_import = CSVimport()
        csv_import.import_files_as_dfs()
        csv_import.get_generators()
        #csv_import.import_csv_files()
