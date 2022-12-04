import os.path

import matplotlib.pyplot as plt
import networkx as nx
from numpy import genfromtxt
import numpy as np
import pandas as pd


def execute_show(outputdir: str, filename: str):
    show_graph_with_labels(os.path.join(outputdir, filename))


def show_graph_with_labels(filename: str):
    data = genfromtxt(filename, delimiter=',')
    df = pd.read_csv(filename)
    labels = list(df.columns[1:])
    adjacency_matrix = data[1:, 1:]
    max_lookups = [0 for i in range(len(labels))]
    for idx, label in enumerate(labels):
        max_lookups[idx] = adjacency_matrix[idx].max()
    gr = nx.Graph()
    for data_item_index, data_item in enumerate(adjacency_matrix):
        for label_index, label in enumerate(labels):
            if label_index != data_item_index and data_item[label_index] >= 1:
                gr.add_edge(labels[data_item_index], labels[label_index], weight=data_item[label_index])
    print("Added data to graph, total edges: " + str(len(gr.edges)))

    edges_for_plot = [(u, v, d) for (u, v, d) in gr.edges(data=True)]
    pos = nx.spectral_layout(gr)
    nx.draw_networkx_nodes(gr, pos, node_size=500)
    for idx, plot_edge in enumerate(edges_for_plot):
        plot_edge_start_node_index = labels.index(plot_edge[0])
        plot_edge_end_node_index = labels.index(plot_edge[1])
        max_node_edge_weight = max_lookups[plot_edge_start_node_index] \
            if max_lookups[plot_edge_start_node_index] > max_lookups[plot_edge_end_node_index] \
            else max_lookups[plot_edge_end_node_index]
        nx.draw_networkx_edges(gr, pos, edgelist=[plot_edge],
                               width=((plot_edge[2].get('weight')/max_node_edge_weight)*2)**2)
        print("Processed " + str(idx) + " of " + str(len(edges_for_plot)) + " edges")
    nx.draw_networkx_labels(gr, pos, font_size=6)
    plt.show()

