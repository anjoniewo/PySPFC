import csv
import os


def check_dir(dir):
    """
    check if dir exists, if not, make it
    :param dir:
    :return:
    """
    directory = os.path.dirname(dir)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_names():
    """
    reads a defined list of required file names for running the simplepowerflow2 tool
    :param file_path: simplepowerflow2/import_file_names.csv
    :return: a set of the file names
    """
    file_path = os.path.join(os.path.dirname(__file__), '../../import_file_names.csv')
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")

        file_names = dict()

        for row in csv_reader:
            file_names[row[0]] = row[1]

    return file_names
