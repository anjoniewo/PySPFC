import matplotlib.pyplot as plt
from simpleloadflow.loadflowtool.utils.config import TITLE_FONTSIZE, LABEL_FONTSIZE

plt.rcParams["font.family"] = "Arial"


def create_voltage_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa", y_axis_label="ordinate"):
	fig, voltage_axes = plt.subplots()
	
	# Spannungsband
	voltage_range_min = 0.9
	voltage_range_max = 1.1
	voltage_axes.axhline(voltage_range_max, color='r', linestyle='--', label='Umax')
	voltage_axes.axhline(voltage_range_min, color='r', linestyle='--', label='Umin')
	
	# Balkendiagramm erstellen
	volt_rects = voltage_axes.bar(x_vals, y_vals, width=0.5, label='Knotenspannung', color='#0090ff')
	
	# Titel des Diagramms
	voltage_axes.set_title(title, fontsize=TITLE_FONTSIZE)
	
	# Y-Achsentitel
	voltage_axes.set_ylabel(y_axis_label, fontsize=LABEL_FONTSIZE, labelpad=15)
	
	# min, max Y-Achse
	temp_y_min = min(y_vals)
	temp_y_max = max(y_vals)
	rel_max_delta = 1.1
	
	if temp_y_min < voltage_range_min:
		y_min = temp_y_min - (temp_y_max * (rel_max_delta - 1))
	else:
		y_min = voltage_range_min - (voltage_range_max * (rel_max_delta - 1))
	
	if temp_y_max < voltage_range_max:
		y_max = voltage_range_max * rel_max_delta
	else:
		y_max = temp_y_max * rel_max_delta
	
	voltage_axes.set_ylim(y_min, y_max)
	
	# X-Achsentitel
	voltage_axes.set_xlabel(x_axis_label, fontsize=LABEL_FONTSIZE, labelpad=10)
	
	# X-Achsenbeschriftungen
	voltage_axes.set_xticks(x_vals)
	
	# absolute max. Werte der einzelnen Balken
	autolabel(volt_rects, voltage_axes, 3)
	
	labels = ['$\pm$ 10 % ${U}_{ref}$', 'Knotenspannung']
	handles, _ = voltage_axes.get_legend_handles_labels()
	
	# Slice list to remove first handle
	voltage_axes.legend(handles=handles[1:], labels=labels)
	
	plt.subplots_adjust(left=0.175, bottom=0.15)
	plt.savefig('..\\..\\test\\test_export\\' + title + '.png', format='png', dpi=120)
	plt.clf()
	plt.cla()


def create_current_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa", y_axis_label="ordinate"):
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
