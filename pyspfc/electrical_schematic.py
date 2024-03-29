import os

import matplotlib.pyplot as plt
import networkx as nx

from pyspfc.directories import get_schematic_export_path, IMG_FILE_EXTENSION


def create_network_schematic(grid_lines, transformers):
    G = nx.Graph()
    plt.tight_layout()

    edges_labels = dict()

    for grid_line in grid_lines:
        grid_node_i = grid_line.get_node_name_i()
        grid_node_j = grid_line.get_node_name_j()

        edges_labels_dict_tup = (grid_node_i, grid_node_j)
        edges_labels[edges_labels_dict_tup] = grid_line.name

        G.add_edge(grid_node_i, grid_node_j, weight=0.1)

    for transformer in transformers:
        grid_node_i = transformer.get_node_name_i()
        grid_node_j = transformer.get_node_name_j()

        G.add_edge(grid_node_i, grid_node_j, weight=0.1)

    pos = nx.circular_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=1200, node_color='#a7e7a2', linewidths=1.5, edgecolors='#18b40c')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=3, edge_color='#9f9ea7', edges_labels=edges_labels)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges_labels, font_size=14)

    plt.axis('off')
    title = 'network_schematic'
    file_name = str(title + IMG_FILE_EXTENSION)
    file_path_name = os.path.join(get_schematic_export_path(), file_name)
    plt.savefig(file_path_name, format='png', dpi=120)
    plt.clf()
    plt.cla()
