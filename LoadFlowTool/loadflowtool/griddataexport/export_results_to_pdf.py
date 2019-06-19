from fpdf import FPDF

title = 'Lastflussberechnung-Ergebnisse'


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
		self.cell(0, 10, 'Seite ' + str(self.page_no()), 0, 0, 'C')
	
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
		txt = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
		
		# Read text file
		# with open(name, 'rb') as fh:
		#     txt = fh.read().decode('latin-1')
		# Times 12
		self.set_font('Times', '', 12)
		# Output justified text
		self.multi_cell(0, 5, txt)
		# Line break
		self.ln()
		# Mention in italics
		self.set_font('', 'I')
		self.cell(0, 5, '(end of excerpt)')
	
	def print_chapter(self, num, title, name, has_body=False):
		self.add_page()
		self.chapter_title(num, title)
		if has_body: self.chapter_body(name)


def convert_data_to_table_data(data):
	"""
		Funktion konvertiert ein Dictionary von Dictionaries in eine Liste von Listen
	:param data:
	:return:
	"""
	list_of_lists = list(list())
	header = ['Name', 'Typ', 'P_L', 'P_G', 'P', 'Q_L', 'Q_G', 'Q', '|U|', 'U-Winkel']
	list_of_lists.append(header)
	
	for key, value in data.items():
		sub_list = list()
		sub_list.append(key)
		for sub_key, sub_value in value.items():
			if isinstance(sub_value, float):
				sub_value = round(float(sub_value), 3)
			sub_list.append(sub_value)
		
		list_of_lists.append(sub_list)
	
	return list_of_lists


def create_pdf_report(grid_node_data, grid_line_data):
	grid_node_data = convert_data_to_table_data(grid_node_data)
	grid_line_data = convert_data_to_table_data(grid_line_data)
	
	plot_path = '..\\..\\test\\test_export\\'
	current_plot_path = plot_path + 'Strom pro Leitung.png'
	voltage_plot_path = plot_path + 'Knotenspannung pro Knoten.png'
	
	pdf = PDF()
	pdf.set_title(title)
	pdf.set_author('Christian Klosterhalfen, Anjo Niewöhner')
	
	# Kapitel 1
	pdf.print_chapter(1, title='Netz', name='', has_body=True)
	pdf.ln(16)
	
	# Effective page width, or just epw
	epw = pdf.w - 2 * pdf.l_margin
	# Document title centered, 'B'old, 14 pt
	pdf.set_font('Times', 'B', 14.0)
	pdf.cell(epw, 0.0, 'Tabelle der Knoten - Angabe in p.u. mit U_ref = 220 kV und S_ref = 100 MVA',
	         align='L')
	pdf.ln(4)
	pdf.set_font('Times', '', 12.0)
	pdf.ln(2)
	
	# Effective page width, or just epw
	epw = pdf.w - 2 * pdf.l_margin
	
	# Set column width to 1/4 of effective page width to distribute content
	# evenly across table and page
	col_width = epw / 10
	
	# Text height is the same as current font size
	th = pdf.font_size
	
	""" Ausgabe der Knotentabelle """
	# Here we add more padding by passing 2*th as height
	for row in grid_node_data:
		for col in row:
			# Enter data in colums
			pdf.cell(col_width, 2 * th, str(col), border=1)
		
		pdf.ln(2 * th)
		
	pdf.ln(10)
	pdf.set_font('Times', 'B', 14.0)
	pdf.cell(epw, 0.0, 'Tabelle der Leitungen - Angabe in p.u. mit U_ref = 220 kV und S_ref = 100 MVA',
	         align='L')
	pdf.ln(4)
	pdf.set_font('Times', '', 12.0)
	pdf.ln(2)
	
	""" Ausgabe der Leitungstabelle """
	# Here we add more padding by passing 2*th as height
	for row in grid_node_data:
		for col in row:
			# Enter data in colums
			pdf.cell(col_width, 2 * th, str(col), border=1)
		
		pdf.ln(2 * th)
	
	# Kapitel 2
	pdf.print_chapter(2, title='Diagramme', name='', has_body=False)
	
	x_pos = pdf.w / 6.95
	y_pos = 32
	width = 150
	height = 125
	# add node voltages plot
	pdf.image(voltage_plot_path, x=x_pos, y=y_pos, w=width, h=height, type='', link='')
	
	y_pos = pdf.h / 1.9
	# add line currents plot
	pdf.image(current_plot_path, x=x_pos, y=y_pos, w=width, h=height, type='', link='')
	
	pdf.output('loadflow_report.pdf', 'F')
