"""
This module provides a set of functions for processing NetworkX graphs by removing nodes and edges with specific labels
and saving the processed graphs to various formats. It also offers functions for replacing specific node and edge
labels with default labels and flattening nested lists.
"""

import os
import pickle

directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension

# loop through the directory and get file names with the desired extension
file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)


def remove_nodes_with_label(graph, label)->None:
    """
    Remove nodes from a graph with a specific label.

    :param graph: The NetworkX graph.
    :type graph: nx.Graph
    :param label: The label of nodes to be removed.
    :type label: str
    """
    nodes_to_remove = [node for node, data in graph.nodes(data=True) if data.get('label') == label]
    graph.remove_nodes_from(nodes_to_remove)


def remove_edges_with_label(graph, label)->None:
    """
    Remove edges from a graph with a specific label.

    :param graph: The NetworkX graph.
    :type graph: nx.Graph
    :param label: The label of edges to be removed.
    :type label: str
    """
    edges_to_remove = [(u, v) for u, v, data in graph.edges(data=True) if data.get('label') == label]
    graph.remove_edges_from(edges_to_remove)


def process_graphs(node_labels, edge_labels, graphs):
    """
    Process a list of graphs by removing nodes and edges with specific labels.

    :param node_labels: List of node labels to be removed.
    :type node_labels: list of str
    :param edge_labels: List of edge labels to be removed.
    :type edge_labels: list of str
    :param graphs: List of graph data as tuples containing a name and a NetworkX graph.
    :type graphs: list of tuple
    :return: List of processed NetworkX graphs.
    :rtype: list of nx.Graph
    """

    undirectedgraphs_f = []

    for [i, graph] in graphs:
        for node_label in node_labels:
            remove_nodes_with_label(graph, node_label)

        for edge_label in edge_labels:
            remove_edges_with_label(graph, edge_label)

        undirectedgraphs_f.append(graph)

    return undirectedgraphs_f


def process_graphs_with_names(node_labels, edge_labels, graphs):
    """
    Process a list of graphs by removing nodes and edges with specific labels, preserving graph names.

    :param node_labels: List of node labels to be removed.
    :type node_labels: list of str
    :param edge_labels: List of edge labels to be removed.
    :type edge_labels: list of str
    :param graphs: List of graph data as tuples containing a name and a NetworkX graph.
    :type graphs: list of tuple
    :return: List of processed graph data with names and NetworkX graphs.
    :rtype: list of tuple
    """

    undirectedgraphs_f = []

    for [i, graph] in graphs:
        for node_label in node_labels:
            remove_nodes_with_label(graph, node_label)

        for edge_label in edge_labels:
            remove_edges_with_label(graph, edge_label)

        undirectedgraphs_f.append([i, graph])

    return undirectedgraphs_f


def process_graphs_(node_labels, edge_labels, graphs):
    """
    Process a list of graphs by removing nodes and edges with specific labels, preserving additional data.

    :param node_labels: List of node labels to be removed.
    :type node_labels: list of str
    :param edge_labels: List of edge labels to be removed.
    :type edge_labels: list of str
    :param graphs: List of graph data as tuples containing support, index, and a NetworkX graph.
    :type graphs: list of tuple
    :return: List of processed graph data with support, index, and NetworkX graphs.
    :rtype: list of tuple
    """

    undirectedgraphs_f = []

    for [support, index, graph] in graphs:
        for node_label in node_labels:
            remove_nodes_with_label(graph, node_label)

        for edge_label in edge_labels:
            remove_edges_with_label(graph, edge_label)

        undirectedgraphs_f.append([support, index, graph])

    return undirectedgraphs_f


def process_graphs__(node_labels, edge_labels, graphs):
    """
    Process a list of graphs by removing nodes and edges with specific labels, preserving index dictionary.

    :param node_labels: List of node labels to be removed.
    :type node_labels: list of str
    :param edge_labels: List of edge labels to be removed.
    :type edge_labels: list of str
    :param graphs: List of graph data as tuples containing index dictionary and a NetworkX graph.
    :type graphs: list of tuple
    :return: List of processed graph data with index dictionary and NetworkX graphs.
    :rtype: list of tuple
    """

    undirectedgraphs_f = []

    for [index_dict, graph] in graphs:
        for node_label in node_labels:
            remove_nodes_with_label(graph, node_label)

        for edge_label in edge_labels:
            remove_edges_with_label(graph, edge_label)

        undirectedgraphs_f.append([index_dict, graph])

    return undirectedgraphs_f


def replace_labels_with_default(class_labels, relation_labels, edge_labels, graphs):
    """
    Replace specific node and edge labels with default labels in a list of graphs.

    :param class_labels: List of class labels to be replaced.
    :type class_labels: list of str
    :param relation_labels: List of relation labels to be replaced.
    :type relation_labels: list of str
    :param edge_labels: List of edge labels to be removed.
    :type edge_labels: list of str
    :param graphs: List of NetworkX graphs to be processed.
    :type graphs: list of nx.Graph
    :return: List of processed NetworkX graphs.
    :rtype: list of nx.Graph
    """

    # Create a mapping for node and edge labels
    class_mapping = {label: "class" for label in class_labels}
    relation_mapping = {label: "relation" for label in relation_labels}

    # Process each graph
    for graph in graphs:
        # Replace labels
        for node in graph.nodes():
            graph.nodes[node]['label'] = class_mapping.get(graph.nodes[node]['label'], graph.nodes[node]['label'])
            graph.nodes[node]['label'] = relation_mapping.get(graph.nodes[node]['label'], graph.nodes[node]['label'])
        # Remove edges
        for edge_label in edge_labels:
            remove_edges_with_label(graph, edge_label)

    return graphs


def save_graphs_to_pickle(graphs, filename)->None:
    """
    Save a list of NetworkX graphs to a pickle file in a specific folder.
    
    :param graphs: List of NetworkX graphs.
    :type graphs: list of nx.Graph
    :param filename: Name of the pickle file including the folder path.
    :type filename: str
    """
    folder_path = os.path.dirname(filename)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(filename, 'wb') as file:
        pickle.dump(graphs, file)


def flatten(lst):
    """
    Flatten a nested list into a single list.

    :param lst: The nested list to be flattened.
    :type lst: list
    :return: The flattened list.
    :rtype: list
    """
    if isinstance(lst, list):
        return [elem for sublist in lst for elem in flatten(sublist)]
    else:
        return [lst]


def graphs_to_data_file(graphs, name)->None:
    """
    Write graph data to a data file in the specified format.

    :param graphs: List of graph data as tuples containing a name and a NetworkX graph.
    :type graphs: list of tuple
    :param name: Name of the data file.
    :type name: str
    """
    with open("input/" + name + ".data", "w") as f:
        # Write the graphs
        for i, [n, G] in enumerate(graphs):
            # Write the graph header
            f.write(f"t # {i} {n}\n")

            # Write the nodes
            nodes_list = list(G.nodes())
            for node in nodes_list:
                node_index = nodes_list.index(node) + 1
                node_label = G.nodes()[node]["label"] if "label" in G.nodes()[node] else "None"
                f.write(f"v {node_index} {node_label}\n")

            # Write the edges
            for edge in G.edges(data=True):
                source_index = nodes_list.index(edge[0]) + 1
                target_index = nodes_list.index(edge[1]) + 1
                edge_label = edge[2]["label"] if "label" in edge[2] else "None"
                f.write(f"e {source_index} {target_index} {edge_label}\n")
