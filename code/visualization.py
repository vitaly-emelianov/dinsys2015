import networkx as nx
from networkx import graphviz_layout
from matplotlib import pyplot as plt


def visualize(tree, custom_alpha=0.5, labels=False):
    G = nx.Graph(tree)
    pos = nx.graphviz_layout(G, prog='twopi', args='', root='root')
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, node_size=0, alpha=custom_alpha, node_color="blue", with_labels=labels)
    plt.axis('equal')
    plt.show()
