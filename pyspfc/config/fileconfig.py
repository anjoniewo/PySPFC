import csv
import os


def check_dir(dir):
    """
    check if dir exists, if not, make it
    :param dir:
    :return:
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_file_names():
    """
    reads a defined list of required file names for running the simplepowerflow2 tool
    :param file_path: simplepowerflow2/import_file_names.csv
    :return: a set of the file names
    """
    from pyspfc.directories import get_filenames_path
    with open(get_filenames_path(), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")

        file_names = dict()

        for row in csv_reader:
            file_names[row[0]] = row[1]

    return file_names
