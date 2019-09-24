#   Copyright (C) 2019  Christian Klosterhalfen (TH Köln), Anjo Niewöhner (TH Köln)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import csv
import os


def check_dir_and_delete(directory):
    """
    check if directory exists, if not, create it
    :param directory: directory that will be checked
    :return: none
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        files = os.listdir(directory)
        for file in files:
            os.remove(os.path.join(directory, file))


def check_dir(directory):
    """
    check if directory exists, if not, create it
    :param directory: directory that will be checked
    :return: none
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_file_names():
    """
    reads a defined list of required file names for running the pyspfc tool
    :param file_path: pyspfc/config/import_file_names.csv
    :return: a set of the file names
    """
    from pyspfc.directories import get_filenames_path
    with open(get_filenames_path(), mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")

        file_names = dict()

        for row in csv_reader:
            file_names[row[0]] = row[1]

    return file_names
