import os
import platform

from .config.fileconfig import check_dir

"""
defined constants for PySPFC
"""

TITLE_FONTSIZE = 16
LABEL_FONTSIZE = 14
TICK_FONTSIZE = 12

BAR_COLOR = 'red'

operating_system = platform.system()
WINDOWS = 'Windows'
LINUX = 'Linux'
MAC_OS = 'Darwin'
OS_SLASH = str('/') if operating_system == MAC_OS or operating_system == LINUX else str('\\')

DEFAULT_ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
WAS_ROOT_PATH_RESETED = False
CSV_FILE_EXTENSION = '.csv'
PDF_FILE_EXTENSION = '.pdf'
IMG_FILE_EXTENSION = '.png'
TIMESTAMP = str('timestamp')


def get_root_path():
    """
    get the directory of export path
    :return: directory as a string
    """
    root_path = os.path.join(DEFAULT_ROOT_PATH)
    check_dir(root_path)
    return root_path


def get_import_path():
    """
    get the directory of import path
    :return: directory as a string
    """
    return get_root_path() + OS_SLASH + 'csv_import' if WAS_ROOT_PATH_RESETED is False else get_root_path()


def get_export_path():
    """
    get the directory of export path
    :return: directory as a string
    """
    export_path = os.path.join(get_root_path(), 'export')
    check_dir(export_path)
    return export_path


def get_csv_export_path():
    """
    get the directory of csv export path
    :return: directory as a string
    """
    csv_export_path = os.path.join(get_export_path(), 'csv')
    check_dir(csv_export_path)
    return csv_export_path


def get_plot_export_path():
    """
    get the directory of plot export path
    :return: directory as a string
    """
    plot_path_export = os.path.join(get_export_path(), 'plots')
    check_dir(plot_path_export)
    return plot_path_export


def get_pdf_export_path():
    """
    get the directory of pdf export path
    :return: directory as a string
    """
    pdf_export_path = os.path.join(get_export_path(), 'pdf')
    check_dir(pdf_export_path)
    return pdf_export_path


def get_schematic_export_path():
    """
    get the directory of schematic export path
    :return: directory as a string
    """
    schematic_export_path = os.path.join(get_export_path(), 'network_schematic')
    check_dir(schematic_export_path)
    return schematic_export_path


def get_pyspfc_path():
    """
    get the directory of pyspfc path
    :return: directory as a string
    """
    pyspfc_path = os.path.join(get_root_path(), 'pyspfc')
    check_dir(pyspfc_path)
    return pyspfc_path


def get_config_path():
    """
    get the directory of config path
    :return: directory as a string
    """
    config_path = os.path.join(get_pyspfc_path(), 'config')
    check_dir(config_path)
    return config_path


def get_filenames_path():
    """
    get the directory of 'import_file_names.csv' file
    :return: directory as a string
    """
    filenames_csv_path = os.path.join(get_config_path(), 'import_file_names.csv')
    return filenames_csv_path


def reset_root_path(root_path=''):
    """
    Function resets the export path
    :param root_path: specified path
    :return: none
    """
    global DEFAULT_ROOT_PATH
    DEFAULT_ROOT_PATH = root_path
    global WAS_ROOT_PATH_RESETED
    WAS_ROOT_PATH_RESETED = True
