import os
import platform

from simplepowerflow.config.fileconfig import check_dir

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

ROOT_PATH = os.path.dirname(__file__)
EXPORT_PATH = os.path.join(ROOT_PATH, 'export')
check_dir(EXPORT_PATH)
CSV_EXPORT_PATH = os.path.join(EXPORT_PATH, 'csv')
check_dir(CSV_EXPORT_PATH)
PLOT_EXPORT_PATH = os.path.join(EXPORT_PATH, 'plots')
check_dir(PLOT_EXPORT_PATH)
PDF_EXPORT_PATH = os.path.join(EXPORT_PATH, 'pdf')
check_dir(PDF_EXPORT_PATH)
SCHEMATIC_EXPORT_PATH = os.path.join(EXPORT_PATH, 'network_schematic')
check_dir(SCHEMATIC_EXPORT_PATH)
SIMPLEPOWERFLOW_PATH = os.path.join(ROOT_PATH, 'simplepowerflow')
CONFIG_PATH = os.path.join(SIMPLEPOWERFLOW_PATH, 'config')
check_dir(CONFIG_PATH)
FILENAMES_CSV_PATH = os.path.join(CONFIG_PATH, 'import_file_names.csv')
CSV_FILE_EXTENSION = '.csv'
PDF_FILE_EXTENSION = '.pdf'
PNG_FILE_EXTENSION = '.png'
TIMESTAMP = str('timestamp')
