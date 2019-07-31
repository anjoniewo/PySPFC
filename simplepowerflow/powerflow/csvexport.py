import os

from simplepowerflow.powerflow.griddataexport.export_gridline_data import export_data_to_csv

csv_export_path = os.path.join(os.path.dirname(__file__), '..\\csv_export')


class CSVexport:
	
	def __init__(self):
		pass
	
	def export_currents_on_lines_plot(self):
		1
	
	# # die X-Werte:
	# grid_lines = list()
	# # die Y-Werte:
	# current_on_lines = list()
	#
	# for grid_line_name in self.grid_line_results:
	#     grid_lines.append(grid_line_name)
	#     current_on_lines.append(self.grid_line_results[grid_line_name]["current_from_i_to_j"])
	#
	# current_nom = self.s_nom / (self.v_nom * math.sqrt(3))
	# current_on_lines = list(map(lambda value: value * current_nom, current_on_lines))
	#
	# create_current_plot(grid_lines, current_on_lines, "Strom pro Leitung", "Leitung k", "Strom in A")
	
	def export_node_voltage_plot(self):
		1
	
	# # die X-Werte:
	# grid_nodes = list()
	# # die Y-Werte:
	# node_voltages = list()
	#
	# for grid_node_name in self.grid_node_results:
	#     grid_nodes.append(grid_node_name)
	#     node_voltages.append(self.grid_node_results[grid_node_name]["U_magnitude"])
	#
	# create_voltage_plot(grid_nodes, node_voltages, "Betrag der Knotenspannung", "Knoten n", "Spannung in pu")
	
	def export_grid_node_results(self, timestamps, grid_node_results):
		"""
		method exports node results to csv files in a specified directory (csv_export_path)
		:param csv_export_path:
		:return:
		"""
		
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
					p_load[key].append(str(value['p_load']))
				if 'q_load' in value:
					q_load[key].append(str(value['q_load']))
				if 'p_gen' in value:
					p_gen[key].append(str(value['p_gen']))
				if 'q_gen' in value:
					q_gen[key].append(str(value['q_gen']))
				if 'v_magnitude' in value:
					v_mag[key].append(str(value['v_magnitude']))
				if 'v_angle' in value:
					v_angle[key].append(str(value['v_angle']))
		
		export_data_to_csv(csv_export_path, "p_loads", p_load)
		export_data_to_csv(csv_export_path, "q_loads", q_load)
		export_data_to_csv(csv_export_path, "p_generators", p_gen)
		export_data_to_csv(csv_export_path, "q_generators", q_gen)
		export_data_to_csv(csv_export_path, "v_magnitudes", v_mag)
		export_data_to_csv(csv_export_path, "v_angles", v_angle)
	
	def export_grid_line_results(self, timestamps, grid_line_results):
		"""
		method exports node results to csv files in a specified directory (csv_export_path)
		:param csv_export_path:
		:return:
		"""
		
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
					p_over_lines[key].append(str(value['p_from_i_to_j']))
				if 'q_from_i_to_j' in value:
					q_over_lines[key].append(str(value['q_from_i_to_j']))
				if 's_from_i_to_j' in value:
					s_over_lines[key].append(str(value['s_from_i_to_j']))
				if 'p_loss' in value:
					p_transmission_losses[key].append(str(value['p_loss']))
				if 'q_loss' in value:
					q_transmission_losses[key].append(str(value['q_loss']))
				if 'current_from_i_to_j' in value:
					line_currents[key].append(str(value['current_from_i_to_j']))
		
		export_data_to_csv(csv_export_path, "p_lines", p_over_lines)
		export_data_to_csv(csv_export_path, "q_lines", q_over_lines)
		export_data_to_csv(csv_export_path, "s_lines", s_over_lines)
		export_data_to_csv(csv_export_path, "p_transmission_losses", p_transmission_losses)
		export_data_to_csv(csv_export_path, "q__transmission_losses", q_transmission_losses)
		export_data_to_csv(csv_export_path, "current_on_lines", line_currents)
