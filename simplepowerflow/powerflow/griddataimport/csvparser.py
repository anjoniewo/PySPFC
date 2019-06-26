import csv
from collections import defaultdict


# CSV-Parser-Klasse (wird von gridlineparser und gridnodeparser geerbt)
class CSVParser:

    def __init__(self):
        # Liste fuer die 1. Zeile der einzulesenden CSV-Datei
        self.header_row = []

        # Dictionary in dem die CSV-Daten gespeichert werden
        # key = Spaltenbezeichnung (also die Elemente von self.header_row)
        # value = Liste der Spaltenwerte

        self.csv_dictionary = defaultdict(list)

    pass

    # Methode die eine bestimmte CSV-Datei einliest
    def read_csv_to_dictionary(self, file_path):
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")

            # Zaehler fuer die Zeilen in der CSV-Datei
            line_count = 0

            for row in csv_reader:
                # 1. Zeile der CSV-Datei
                if line_count == 0:
                    # Werte der 1. Zeile als Liste speichern
                    self.header_row = row

                    # die Ueberschriftenliste durchgehen
                    for entry in self.header_row:
                        # jedes Element der Ueberschriftenliste wird der key des Dictionaries
                        self.csv_dictionary[entry] = []

                # alle weiteren Zeilen
                else:
                    for index, entry in enumerate(row):
                        # falls der key enthalten ist
                        if self.header_row[index] in self.csv_dictionary:
                            # values des Dictionaries fuellen
                            self.csv_dictionary[self.header_row[index]].append(row[index])

                line_count += 1
