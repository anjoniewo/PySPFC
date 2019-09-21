import math
import os

from fpdf import FPDF

from pyspfc.directories import PDF_FILE_EXTENSION, get_pdf_export_path, get_plot_export_path, get_schematic_export_path

title = 'PySPFC - Results Report'


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 16)
        # Calculate width of title and position
        w = self.get_string_width(title) + 10
        # self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        # self.set_draw_color(0, 80, 180)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        # Thickness of frame (1 mm)
        self.set_line_width(1)
        # Title
        self.cell(0, 9, title, 0, 1, 'C', 1)
        # Line break
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', style='', size=8)
        # Text color in gray
        self.set_text_color(0)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        # Arial 12
        self.set_font('Arial', '', 12)
        # Background color
        self.set_fill_color(226, 226, 226)
        # Title
        self.cell(0, 6, label, 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, name):
        txt = 'Schematic of the electrical grid'

        # Read text file
        # with open(name, 'rb') as fh:
        #     txt = fh.read().decode('latin-1')
        # Times 12
        self.set_font('Arial', 'B', 12)
        # Output justified text
        self.multi_cell(0, 5, txt)
        # Line break
        self.ln()
        # Mention in italics
        self.set_font('', 'I')

    def print_chapter(self, num, title, name, has_body=False, pdf=None):
        self.add_page()
        self.chapter_title(num, title)
        if has_body:
            pdf.ln(4)
            self.chapter_body(name)


def create_pdf_report(grid_node_data=dict(), grid_line_data=dict(), v_nom=0, s_nom=0):
    timeseries_current_plot_path = os.path.join(get_plot_export_path(), 'Time variant Current on lines.png')
    timeseries_voltage_plot_path = os.path.join(get_plot_export_path(), 'Time variant Bus voltages.png')
    min_voltage_plot_path = os.path.join(get_plot_export_path(), 'Bus Voltages at minimal Grid Load.png')
    max_voltage_plot_path = os.path.join(get_plot_export_path(), 'Bus Voltages at maximal Grid Load.png')
    min_line_plot_path = os.path.join(get_plot_export_path(), 'Current on Lines at minimal Grid Load.png')
    max_line_plot_path = os.path.join(get_plot_export_path(), 'Current on Lines at maximal Grid Load.png')
    network_schematic_path = os.path.join(get_schematic_export_path(), 'network_schematic.png')

    pdf = PDF()
    pdf.set_margins(top=10, left=16)
    pdf.set_title(title)
    pdf.set_author('Christian Klosterhalfen, Anjo Niewöhner')

    # chapter 1
    pdf.print_chapter(1, title='Grid', name='', has_body=True, pdf=pdf)

    # add network schematic
    x_pos = pdf.w / 5
    y_pos = 50
    width = pdf.w / 2
    height = 80
    pdf.image(network_schematic_path, x=x_pos, y=y_pos, w=width, h=height)
    pdf.ln(70)

    # chapter 2
    pdf.print_chapter(2, title='Stationary Load Flow Calculation Results', name='')
    pdf.ln(7)

    # effective page width, or just epw
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 11
    text_height = pdf.font_size

    # add tables of minimal grid load penetration
    min_grid_node_data = convert_data_to_table_data(grid_node_data['max'])
    # ------------------------------------------------------------------------------------------------------------------
    table_label = 'Table of buses at minimal Grid Load - V_ref = ' + str(v_nom) + ' kV and S_ref = ' + str(
        int(s_nom / 1e3)) + ' MVA'
    add_table(pdf=pdf, table_label=table_label, tab_lab_height=epw, data=min_grid_node_data, width=col_width,
              height=2 * text_height)
    pdf.ln(1)
    table_legend = 'L: load, G: generation'
    pdf.cell(epw, text_height, str(table_legend), align='L')
    # ------------------------------------------------------------------------------------------------------------------

    pdf.ln(14)

    min_grid_line_data = convert_data_to_table_data(grid_line_data['max'], type='line', v_nom=v_nom, s_nom=s_nom)
    # ------------------------------------------------------------------------------------------------------------------
    table_label = 'Table of lines minimal Grid Load - data in physical values'
    add_table(pdf=pdf, table_label=table_label, tab_lab_height=epw, data=min_grid_line_data, width=col_width * 2,
              height=2 * text_height)
    pdf.ln(1)
    table_legend = 'i: bus at start, j: bus at end'
    pdf.cell(epw, text_height, str(table_legend), align='L')
    # ------------------------------------------------------------------------------------------------------------------

    pdf.ln(14)

    # add tables of maximal grid load penetration
    max_grid_node_data = convert_data_to_table_data(grid_node_data['min'])
    # ------------------------------------------------------------------------------------------------------------------
    table_label = 'Table of buses at maximal Grid Load - V_ref = ' + str(v_nom) + ' kV and S_ref = ' + str(
        int(s_nom / 1e3)) + ' MVA'
    add_table(pdf=pdf, table_label=table_label, tab_lab_height=epw, data=max_grid_node_data, width=col_width,
              height=2 * text_height)
    pdf.ln(1)
    table_legend = 'L: load, G: generation'
    pdf.cell(epw, text_height, str(table_legend), align='L')
    # ------------------------------------------------------------------------------------------------------------------

    pdf.ln(14)

    max_grid_line_data = convert_data_to_table_data(grid_line_data['min'], type='line', v_nom=v_nom, s_nom=s_nom)
    # ------------------------------------------------------------------------------------------------------------------
    table_label = 'Table of lines maximal Grid Load - data in physical values'
    add_table(pdf=pdf, table_label=table_label, tab_lab_height=epw, data=max_grid_line_data, width=col_width * 2,
              height=2 * text_height)
    pdf.ln(1)
    table_legend = 'i: bus at start, j: bus at end'
    pdf.cell(epw, text_height, str(table_legend), align='L')
    # ------------------------------------------------------------------------------------------------------------------

    # chapter 3 --------------------------------------------------------------------------------------------------------
    pdf.print_chapter(3, title='Time variant Plots', name='')

    x_pos = pdf.w / 6.95
    y_pos = 32
    width = 150
    height = 125

    # add node voltages plot
    pdf.image(timeseries_voltage_plot_path, x=x_pos, y=y_pos, w=width, h=height)

    y_pos = pdf.h / 1.9
    # add line currents plot
    pdf.image(timeseries_current_plot_path, x=x_pos, y=y_pos, w=width, h=height)
    # ------------------------------------------------------------------------------------------------------------------

    # chapter 4 --------------------------------------------------------------------------------------------------------
    pdf.print_chapter(4, title='Plots At Minimal Grid Load', name='')

    x_pos = pdf.w / 6.95
    y_pos = 32
    width = 150
    height = 125

    # add node voltages plot
    pdf.image(min_voltage_plot_path, x=x_pos, y=y_pos, w=width, h=height)

    y_pos = pdf.h / 1.9
    # add line currents plot
    pdf.image(min_line_plot_path, x=x_pos, y=y_pos, w=width, h=height)
    # ------------------------------------------------------------------------------------------------------------------

    # chapter 5 --------------------------------------------------------------------------------------------------------
    pdf.print_chapter(5, title='Plots At maximal Grid Load', name='')

    x_pos = pdf.w / 6.95
    y_pos = 32
    width = 150
    height = 125

    # add node voltages plot
    pdf.image(max_voltage_plot_path, x=x_pos, y=y_pos, w=width, h=height)

    y_pos = pdf.h / 1.9
    # add line currents plot
    pdf.image(max_line_plot_path, x=x_pos, y=y_pos, w=width, h=height)
    pdf_title = 'PowerFlow_Report'
    file_name = pdf_title + PDF_FILE_EXTENSION
    file_path_name = os.path.join(get_pdf_export_path(), file_name)
    pdf.output(file_path_name, 'F')


def convert_data_to_table_data(data, type='node', v_nom=0, s_nom=0):
    """
        Funktion konvertiert ein Dictionary von Dictionaries in eine Liste von Listen
    :param data: data of grid lines or grid nodes to display in a table
    :param type: defines the type of data, can be set to either 'node' or 'line' and affects the header
    :param v_nom: nominal base voltage of the system
    :param s_nom: nominal base power of the system
    :return:
    """

    header = list()
    is_linedata = True if type == 'line' else False

    if not is_linedata:
        header = ['name', 'type', '|P_L|', '|P_G|', 'P', '|Q_L|', '|Q_G|', 'Q', '|U|', 'theta in °']
    elif is_linedata:
        header = ['name', 'bus i', 'bus j', 'P_loss in W', '|I_ij| in A']

        keys_to_delete = list()
        first_key = list(data.keys())[0]
        keys_to_keep = {'bus_i': 0, 'bus_j': 0, 'p_loss': 0, 'current_from_i_to_j': 0}
        for sub_key, sub_value in data[first_key].items():
            if not sub_key in keys_to_keep:
                keys_to_delete.append(sub_key)

        for key, value in data.items():
            for key_to_delete in keys_to_delete:
                del value[key_to_delete]

    table_data_list = list(list())
    table_data_list.append(header)

    for key, value in data.items():
        sub_list = list()
        sub_list.append(key)
        for sub_key, sub_value in value.items():
            if sub_key == 'p_loss':
                if isinstance(sub_value, float):
                    rounded_value = round(float(sub_value * s_nom), 3)
                    sub_value = 0 if abs(rounded_value) == 0 else rounded_value
                sub_list.append(sub_value)
            elif sub_key == 'current_from_i_to_j':
                if isinstance(sub_value, float):
                    rounded_value = round(float(sub_value * (s_nom / (v_nom * math.sqrt(3)))), 3)
                    sub_value = 0 if abs(rounded_value) else rounded_value
                sub_list.append(sub_value)
            else:
                if isinstance(sub_value, float):
                    rounded_value = round(float(sub_value), 3)
                    sub_value = 0 if abs(rounded_value) == 0.0 else rounded_value
                sub_list.append(sub_value)

        table_data_list.append(sub_list)

    return table_data_list


def add_table(pdf=PDF, table_label='Table', tab_lab_height=5, data=list(list()), width=5, height=5,
              font_family='Arial'):
    """
        Method adds a table to a PDF object

    :param pdf: referenced PDF object to be changed
    :param table_label
    :param tab_lab_height
    :param data: List object with table data
    :param width: width of cell
    :param height: height of cell
    :param font_family: Any
    :return: None
    """

    # set the label of the table
    pdf.set_font(font_family, 'B', 12.0)
    pdf.cell(tab_lab_height, 0.0, table_label, align='L')
    pdf.ln(4)

    pdf.set_font(font_family, 'B', 10.0)

    # create header of table
    header_voltage = data.pop(0)
    for item in header_voltage:
        pdf.cell(width, height, str(item), border=1, align='C')

    # line break
    pdf.ln(height)

    pdf.set_font(font_family, '', 10.0)

    # create table
    for row in data:
        for col in row:
            # Enter data in colums
            pdf.cell(width, height, str(col), border=1, align='C')

        pdf.ln(height)
