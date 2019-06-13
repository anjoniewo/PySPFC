import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
# G.add_node("a")
G.add_nodes_from([n for n in range(1, 6)])

G.add_edge(1, 2)
edge = ("d", "e")
G.add_edge(*edge)
edge = ("a", "b")
G.add_edge(*edge)

#print("Nodes of graph: ")
#print(G.nodes())
#print("Edges of graph: ")
#print(G.edges())

# Nodes of graph:
# ['a', 1, 'c', 'b', 'e', 'd', 2]

# Edges of graph:
# [('a', 'b'), (1, 2), ('e', 'd')]

# adding a list of edges:
G.add_edges_from([(1, 2), (3, 4), (1, 5), (4, 5), (1, 2)])

# We can also print the resulting graph by using matplotlib:

nx.draw(G)
# plt.savefig("simple_path.png") # save as png
plt.show()  # display
