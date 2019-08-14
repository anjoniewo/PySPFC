import os

from simplepowerflow.simplepowerflow.utils.config import check_dir

TITLE_FONTSIZE = 16
LABEL_FONTSIZE = 14
TICK_FONTSIZE = 12

BAR_COLOR = 'red'

EXPORT_PATH = os.path.join(os.path.dirname(__file__), '..\\export\\')
check_dir(EXPORT_PATH)
CSV_EXPORT_PATH = EXPORT_PATH + 'csv\\'
check_dir(CSV_EXPORT_PATH)
PLOT_EXPORT_PATH = EXPORT_PATH + 'plots\\'
check_dir(PLOT_EXPORT_PATH)
PDF_EXPORT_PATH = EXPORT_PATH + 'pdf\\'
check_dir(PDF_EXPORT_PATH)
SCHEMATIC_EXPORT_PATH = EXPORT_PATH + 'network_schematic\\'
check_dir(SCHEMATIC_EXPORT_PATH)
