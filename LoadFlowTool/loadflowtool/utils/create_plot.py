import matplotlib.pyplot as plt


def create_plot(x_vals=list(), y_vals=list(), title="title", x_axis_label="abscissa",
                y_axis_label="ordinate"):
    plt.xlabel(x_axis_label, fontsize=16)
    plt.xticks(fontsize=16)
    plt.ylabel(y_axis_label, fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(title, fontsize=20)
    plt.grid(True)
    plt.plot(x_vals, y_vals)
    plt.show()
