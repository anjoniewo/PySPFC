import os

import math
import matplotlib.pyplot as plt

from simplepowerflow.powerflow.griddataexport.export_gridline_data import export_data_to_csv
from simplepowerflow.powerflow.utils.config import LABEL_FONTSIZE, TITLE_FONTSIZE

csv_export_path = os.path.join(os.path.dirname(__file__), '..\\csv_export')
MAX_NUM_OF_NODES = 100


class CSVexport:
	"""
	class to export powerflow results to csv files
	"""
	
	def __init__(self, settings=None):
		self.__settings = settings
	
	def export_currents_on_lines_plot(self, grid_line_results, s_nom, v_nom):
		"""
		@TODO: not yet customized to time series data
		"""
		
		# die X-Werte:
		grid_lines = list()
		# die Y-Werte:
		current_on_lines = list()
		
		for grid_line_name in grid_line_results:
			grid_lines.append(grid_line_name)
			current_on_lines.append(grid_line_results[grid_line_name]["current_from_i_to_j"])
		
		current_nom = s_nom / (v_nom * math.sqrt(3))
		current_on_lines = list(map(lambda value: value * current_nom, current_on_lines))
		
		self.create_current_plot(grid_lines, current_on_lines, "Strom pro Leitung", "Leitung k", "Strom in A")
	
	def export_node_voltage_plot(self, grid_node_results):
		"""
		@TODO: not yet customized to time series data
		"""
		
		if grid_node_results['timestamp']:
			timestamps = dict([(key, value) for key, value in grid_node_results.items() if key == 'timestamp'])
			del grid_node_results['timestamp']
			node_voltages = grid_node_results
			
			x_label = "Timestamps"
			y_label = "Knotenspannungen in pu" if self.__settings.is_export_pu else "Knotenspannungen in kV"
		
		self.create_voltage_plot(x_vals=timestamps, y_vals=node_voltages, title="Betrag der Knotenspannung",
		                         x_axis_label=x_label,
		                         y_axis_label=y_label)
	
	def export_gridnode_results(self, timestamps, grid_node_results):
		
		"""
		method exports node results to csv files in a specified directory (csv_export_path)
		:param csv_export_path:
		:return:
		"""
		
		settings = self.__settings
		v_nom, s_nom = 1 if settings.is_export_pu == 1 else settings.v_nom, settings.s_nom
		
		p_load = {'timestamp': list()}
		q_load = {'timestamp': list()}
		p_gen = {'timestamp': list()}
		q_gen = {'timestamp': list()}
		v_mag = {'timestamp': list()}
		v_angle = {'timestamp': list()}
		for timestamp in timestamps:
			p_load['timestamp'].append(timestamp)
			q_load['timestamp'].append(timestamp)
			p_gen['timestamp'].append(timestamp)
			q_gen['timestamp'].append(timestamp)
			v_mag['timestamp'].append(timestamp)
			v_angle['timestamp'].append(timestamp)
			timestamp_data = grid_node_results[timestamp]
			for key, value in timestamp_data.items():
				if key not in p_load:
					p_load[key] = list()
					q_load[key] = list()
					p_gen[key] = list()
					q_gen[key] = list()
					v_mag[key] = list()
					v_angle[key] = list()
				
				if 'p_load' in value:
					p_load[key].append(str(value['p_load'] * s_nom))
				if 'q_load' in value:
					q_load[key].append(str(value['q_load'] * s_nom))
				if 'p_gen' in value:
					p_gen[key].append(str(value['p_gen'] * s_nom))
				if 'q_gen' in value:
					q_gen[key].append(str(value['q_gen'] * s_nom))
				if 'v_magnitude' in value:
					v_mag[key].append(str(value['v_magnitude'] * v_nom))
				if 'v_angle' in value:
					v_angle[key].append(str(value['v_angle']))
		
		export_data_to_csv(csv_export_path, "p_loads", p_load)
		export_data_to_csv(csv_export_path, "q_loads", q_load)
		export_data_to_csv(csv_export_path, "p_generators", p_gen)
		export_data_to_csv(csv_export_path, "q_generators", q_gen)
		export_data_to_csv(csv_export_path, "v_magnitudes", v_mag)
		export_data_to_csv(csv_export_path, "v_angles", v_angle)
		
		return v_mag
	
	def export_gridline_results(self, timestamps, grid_line_results):
		"""
		method exports node results to csv files in a specified directory (csv_export_path)
		:param csv_export_path:
		:return:
		"""
		
		v_nom, s_nom = 1 if self.__settings.is_export_pu == 1 else self.__settings.v_nom, self.__settings.s_nom
		
		p_over_lines = {'timestamp': list()}
		q_over_lines = {'timestamp': list()}
		s_over_lines = {'timestamp': list()}
		p_transmission_losses = {'timestamp': list()}
		q_transmission_losses = {'timestamp': list()}
		line_currents = {'timestamp': list()}
		for timestamp in timestamps:
			p_over_lines['timestamp'].append(timestamp)
			q_over_lines['timestamp'].append(timestamp)
			s_over_lines['timestamp'].append(timestamp)
			p_transmission_losses['timestamp'].append(timestamp)
			q_transmission_losses['timestamp'].append(timestamp)
			line_currents['timestamp'].append(timestamp)
			timestamp_data = grid_line_results[timestamp]
			for key, value in timestamp_data.items():
				if key not in p_over_lines:
					p_over_lines[key] = list()
					q_over_lines[key] = list()
					s_over_lines[key] = list()
					p_transmission_losses[key] = list()
					q_transmission_losses[key] = list()
					line_currents[key] = list()
				
				if 'p_from_i_to_j' in value:
					p_over_lines[key].append(str(value['p_from_i_to_j'] * s_nom))
				if 'q_from_i_to_j' in value:
					q_over_lines[key].append(str(value['q_from_i_to_j'] * s_nom))
				if 's_from_i_to_j' in value:
					s_over_lines[key].append(str(value['s_from_i_to_j'] * s_nom))
				if 'p_loss' in value:
					p_transmission_losses[key].append(str(value['p_loss'] * s_nom))
				if 'q_loss' in value:
					q_transmission_losses[key].append(str(value['q_loss'] * s_nom))
				if 'current_from_i_to_j' in value:
					line_currents[key].append(str(value['current_from_i_to_j'] * (s_nom / v_nom)))
		
		export_data_to_csv(csv_export_path, "p_lines", p_over_lines)
		export_data_to_csv(csv_export_path, "q_lines", q_over_lines)
		export_data_to_csv(csv_export_path, "s_lines", s_over_lines)
		export_data_to_csv(csv_export_path, "p_transmission_losses", p_transmission_losses)
		export_data_to_csv(csv_export_path, "q__transmission_losses", q_transmission_losses)
		export_data_to_csv(csv_export_path, "current_on_lines", line_currents)
		
		import matplotlib.pyplot as plt
		
		plt.rcParams["font.family"] = "Arial"
	
	def create_voltage_plot(self, x_vals=dict(), y_vals=dict(), title="title", x_axis_label="abscissa",
	                        y_axis_label="ordinate"):
		fig, voltage_axes = plt.subplots()
		
		# Spannungsband
		voltage_range_min = 0.9
		voltage_range_max = 1.1
		voltage_axes.axhline(voltage_range_max, color='r', linestyle='--', label='Umax')
		voltage_axes.axhline(voltage_range_min, color='r', linestyle='--', label='Umin')
		
		if len(y_vals) < MAX_NUM_OF_NODES:
			
			x_vals = x_vals['timestamp']
			
			for key, value in y_vals.items():
				plt.plot(x_vals, value, '-', label=str(key))
		
		# 	# Balkendiagramm erstellen
		# 	volt_rects = voltage_axes.bar(x_vals, y_vals, width=0.5, label='Knotenspannung', color='#0090ff')
		#
		# 	# Titel des Diagramms
		# 	voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)
		#
		# 	# Y-Achsentitel
		# 	voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)
		#
		# 	# min, max Y-Achse
		# 	temp_y_min = min(y_vals)
		# 	temp_y_max = max(y_vals)
		# 	rel_max_delta = 1.1
		#
		# 	if temp_y_min < voltage_range_min:
		# 		y_min = temp_y_min - (temp_y_max * (rel_max_delta - 1))
		# 	else:
		# 		y_min = voltage_range_min - (voltage_range_max * (rel_max_delta - 1))
		#
		# 	if temp_y_max < voltage_range_max:
		# 		y_max = voltage_range_max * rel_max_delta
		# 	else:
		# 		y_max = temp_y_max * rel_max_delta
		#
		# 	voltage_axes.set_ylim(y_min, y_max)
		#
		# 	# X-Achsentitel
		# 	voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)
		#
		# 	# X-Achsenbeschriftungen
		# 	voltage_axes.set_xticks(x_vals)
		#
		# 	# absolute max. Werte der einzelnen Balken
		# 	autolabel(volt_rects, voltage_axes, 3)
		#
		# 	labels = ['$\pm$ 10 % ${U}_{ref}$', 'Knotenspannung']
		# 	handles, _ = voltage_axes.get_legend_handles_labels()
		#
		# # Slice list to remove first handle
		# voltage_axes.legend(handles=handles[1:], labels=labels)
		
		plt.subplots_adjust(left=0.175, bottom=0.15)
		plt.savefig('..\\..\\test\\test_export\\' + title + '.png', format='png', dpi=120)
		plt.clf()
		plt.cla()
	
	def create_current_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
	                        y_axis_label="ordinate"):
		fig, voltage_axes = plt.subplots()
		
		# Balkendiagramm erstellen
		volt_rects = voltage_axes.bar(x_vals, y_vals, width=0.5, label='Strom', color='#ff8a00')
		
		# Titel des Diagramms
		voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)
		
		# Y-Achsentitel
		voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)
		
		# min, max Y-Achse
		temp_y_min = min(y_vals)
		temp_y_max = max(y_vals)
		rel_max_delta = 1.1
		
		y_min = 0
		y_max = temp_y_max * rel_max_delta
		
		voltage_axes.set_ylim(y_min, y_max)
		
		# X-Achsentitel
		voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)
		
		# X-Achsenbeschriftungen
		voltage_axes.set_xticks(x_vals)
		
		# absolute max. Werte der einzelnen Balken
		autolabel(volt_rects, voltage_axes, 0)
		
		voltage_axes.legend()
		
		plt.subplots_adjust(left=0.175, bottom=0.15)
		plt.savefig('..\\..\\test\\test_export\\' + title + '.png', format='png', dpi=120)
		plt.clf()
		plt.cla()


def autolabel(rects, axes, decimals=2, xpos='center'):
	"""
	Attach a text label above each bar in *rects*, displaying its height.

	*xpos* indicates which side to place the text w.r.t. the center of
	the bar. It can be one of the following {'center', 'right', 'left'}.
	"""
	
	ha = {'center': 'center', 'right': 'left', 'left': 'right'}
	offset = {'center': 0, 'right': 1, 'left': -1}
	
	for rect in rects:
		if decimals == 0:
			height = int(round(float(rect.get_height())))
		else:
			height = round(float(rect.get_height()), decimals)
		axes.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
		              xytext=(offset[xpos] * 3, 3),  # use 3 points offset
		              textcoords="offset points",  # in both directions
		              ha=ha[xpos], va='bottom')
