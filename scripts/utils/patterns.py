"""
This Python module provides functions related to working with NetworkX graphs and performing graph mining operations. 
The module includes functions for loading and converting graphs, finding subgraph isomorphisms, removing duplicate graphs, 
and performing various operations on lists of graphs
"""

import networkx as nx
import pickle

def load_graphs_from_pickle(filename):
    """
    Load a list of NetworkX graphs from a pickle file.
    
    Args:
        filename (str): Name of the pickle file.
    
    Returns:
        list: List of NetworkX graphs loaded from the pickle file.
    """
    with open(filename, 'rb') as file:
        graphs = pickle.load(file)
    return graphs

def convertPatterns(path):
    """
    Convert patterns from a file into NetworkX graphs.

    :param path: Path to the file containing patterns.
    :return: List of converted pattern graphs.
    """
    fd = open(path, "r+")
    # sys.stdout = sys.__stdout__
    data = fd.read()
    list_ = data.split("\n")
    fd.close()

    from itertools import groupby

    ####Generate NetworkX Graphs from patterns
    ele = '-----------------' 
    # Group strings at particular element in list
    # using groupby() + list comprehension + lambda
    res = [list(j) for i, j in groupby(list_, lambda x:x == ele) if not i]
    out1 = [[k for k in w if 'Read:' not in k] for w in res]
    out2 = [[k for k in w if 'Mine:' not in k] for w in out1]
    out3 = [[k for k in w if 'Total:' not in k] for w in out2]
    out4 = [[s for s in sub_list if s] for sub_list in out3]
    final_list = list(filter(None, out4))
    #print("Resultant patterns list after grouping : " + str(final_list))

    pattern_graphs = []
    for sublist in final_list:
        # Create a new graph
        G = nx.Graph()
        #G0 = G.to_directed()
        # Iterate over each item in the sublist
        for item in sublist:
            # If the item is a node, add it to the graph
            if item.startswith('v'):
                node_id, node_label = item.split()[1:]
                G.add_node(node_id, label=node_label)
            # If the item is an edge, add it to the graph
            elif item.startswith('e'):
                target, source, edge_label = item.split()[1:]
                G.add_edge(source, target, label=edge_label)
            elif item.startswith('t'):
                s, index = item.split()[1:]
            elif item.startswith('Support:'):
                support = item[9:]
                #G.add_edge(source, target, label=edge_label)
        # Append the graph to the list of graphs
        pattern_graphs.append([{'pattern_support': support,'pattern_index': index},G])
    
    return pattern_graphs

# pattern_graphs = convertPatterns(patternspath)

# def return_all_domain_info(graphs):
#     """
#     Return domain information for each graph.

#     :param graphs: List of pattern graphs.
#     :return: List of processed pattern graphs with domain information.
#     """
#     processed_graphs = []
    
#     for [index_dict,graph] in graphs:
#         new_graph = graph.copy()  # Create a copy of the input graph
        
#         for u, v, label in graph.edges(data='label'):
#             if label in ["source", "target", "general", "specific"]:
#                 if graph.degree(u) == 1:  # Check if u is a leaf node
#                     leaf_node_label = graph.nodes[u].get('label')
#                     if leaf_node_label in ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
#                                            "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
#                                            "creation", "historicalDependence", "manifestation", "participation",
#                                            "participational", "termination", "triggers", "instantiation", "relation"]:
#                         new_node = "n" + str(len(new_graph) + 1)
#                         new_graph.add_edge(u, new_node)  # Add edge between the leaf node and the new node
#                         #new_graph.nodes[new_node]['label'] = ''  # Add a new label to the new node
#                 elif graph.degree(v) == 1:  # Check if v is a leaf node
#                     leaf_node_label = graph.nodes[v].get('label')
#                     if leaf_node_label in ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
#                                            "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
#                                            "creation", "historicalDependence", "manifestation", "participation",
#                                            "participational", "termination", "triggers", "instantiation", "relation"]:
#                         new_node = "n" + str(len(new_graph) + 1)
#                         new_graph.add_edge(v, new_node)  # Add edge between the leaf node and the new node
#                         #new_graph.nodes[new_node]['label'] = ''  # Add a new label to the new node
        
#         processed_graphs.append([index_dict,new_graph])
    
#     return processed_graphs

#new development!!! here we have to add the exact vicino

def return_all_domain_info(graphs):
    """
    Return domain information for each graph.

    :param graphs: List of pattern graphs.
    :return: List of processed pattern graphs with domain information.
    """
    processed_graphs = []

    for index_dict, graph in graphs:
        new_graph = graph.copy()  # Create a copy of the input graph

        for u, v, label in graph.edges(data='label'):
            if label in ["source", "target", "general", "specific"]:
                if graph.degree(u) == 1:  # Check if u is a leaf node
                    leaf_node_label = graph.nodes[u].get('label')
                    if leaf_node_label in ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                                           "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                                           "creation", "historicalDependence", "manifestation", "participation",
                                           "participational", "termination", "triggers", "instantiation", "relation"]:
                        new_node = "n" + str(len(new_graph) + 1)
                        new_graph.add_edge(u, new_node)  # Add edge between the leaf node and the new node
                        # new_graph.nodes[new_node]['label'] = ''  # Add a new label to the new node

                elif graph.degree(u) == 2 and any(graph.get_edge_data(u, neighbor).get('label') in ["cardinalities", "generalization"] for neighbor in graph.neighbors(u)):
                    # Check if u is connected to another node with 'cardinalities' or 'generalization'
                    new_node = "n" + str(len(new_graph) + 1)
                    new_graph.add_edge(u, new_node)

                if graph.degree(v) == 1:  # Check if v is a leaf node
                    leaf_node_label = graph.nodes[v].get('label')
                    if leaf_node_label in ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                                           "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                                           "creation", "historicalDependence", "manifestation", "participation",
                                           "participational", "termination", "triggers", "instantiation", "relation"]:
                        new_node = "n" + str(len(new_graph) + 1)
                        new_graph.add_edge(v, new_node)  # Add edge between the leaf node and the new node
                        # new_graph.nodes[new_node]['label'] = ''  # Add a new label to the new node

                elif graph.degree(v) == 2 and any(graph.get_edge_data(v, neighbor).get('label') in ["cardinalities", "generalization"] for neighbor in graph.neighbors(v)):
                    # Check if v is connected to another node with 'cardinalities' or 'generalization'
                    new_node = "n" + str(len(new_graph) + 1)
                    new_graph.add_edge(v, new_node)

        processed_graphs.append([index_dict, new_graph])

    return processed_graphs



from grandiso import find_motifs

def count_subgraph_isomorphisms(source_graphs, target_graphs):
    """
    Count subgraph isomorphisms between source and target graphs.

    :param source_graphs: List of source graphs.
    :param target_graphs: List of target graphs.
    :return: List of matched subgraph isomorphisms.
    """
    matches_list = []
    # Loop through each source graph and target graph
    for i, [index_dict,source_graph] in enumerate(source_graphs):
        pattern_support = index_dict['pattern_support']
        pattern_index = index_dict['pattern_index']
        for j, target_graph in enumerate(target_graphs):
            # Use find_motifs to find matches
            matches = find_motifs(source_graph, target_graph,isomorphisms_only=False) #directed=True)
            for match in matches:
                # Extract the matched nodes and labels from the target graph
                matched_nodes = list(match.values())
                matched_labels = {node: target_graph.nodes[node] for node in matched_nodes}
                # Create a networkx graph from the matched nodes in the target graph
                matched_graph = target_graph.subgraph(matched_nodes)
                # Extract the nodes, node labels, and edge labels from the matched graph
                nodes = list(matched_graph.nodes())
                node_labels = {node: matched_labels[node] for node in nodes}
                edges = list(matched_graph.edges(data=True))
                edge_labels = {(edge[0], edge[1]): edge[2] for edge in edges}
                # Create a dictionary to store the matched nodes, labels, and graph from the target graph
                #matched_dict = {'source_graph_index': i, 'target_graph_index': j, 'matched_graph': matched_graph, 'nodes': nodes, 'node_labels': node_labels, 'edge_labels': edge_labels}
                matched_dict = [{'pattern_support': pattern_support,'pattern_index': pattern_index,'model_index': j}, matched_graph]
                matches_list.append(matched_dict)
    return matches_list

# ################clean_lists################

import networkx as nx
from grandiso import find_motifs

def remove_duplicate_graphs(graphs):
    """
    Remove duplicate graphs from a list of graphs.

    :param graphs: List of graphs.
    :return: List of unique graphs after removing duplicates.
    """
    unique_graphs = []
    graph_hashes = {}

    for i, (index_dict, G) in enumerate(graphs):
        pattern_support = index_dict['pattern_support']
        pattern_index = index_dict['pattern_index']
        model_index = index_dict['model_index']

        # Create a composite key using both pattern_index and model_index
        composite_key = (pattern_index, model_index)

        if composite_key not in graph_hashes:
            graph_hashes[composite_key] = set()

        # Calculate the hash value for the graph based on the specified attributes
        graph_hash = (
            len(G.nodes),
            len(G.edges),
            tuple(sorted(nx.get_node_attributes(G, 'label').values())),
            tuple(sorted(nx.get_node_attributes(G, 'label0').values())),
            tuple(sorted(nx.get_edge_attributes(G, 'label').values()))
        )

        # Check if the hash value is already seen within the same pattern_index and model_index
        if graph_hash not in graph_hashes[composite_key]:
            # Check if any previously seen graph within the same pattern_index and model_index
            # has the same number of nodes and edges, as well as the same label and label0 values
            is_duplicate = False
            for existing_graph in unique_graphs:
                existing_index_dict, existing_G = existing_graph
                existing_pattern_index = existing_index_dict['pattern_index']
                existing_model_index = existing_index_dict['model_index']

                if (
                    existing_pattern_index == pattern_index
                    and existing_model_index == model_index
                    and len(existing_G.nodes) == len(G.nodes)
                    and len(existing_G.edges) == len(G.edges)
                    and sorted(nx.get_node_attributes(existing_G, 'label').values())
                    == sorted(nx.get_node_attributes(G, 'label').values())
                    and sorted(nx.get_node_attributes(existing_G, 'label0').values())
                    == sorted(nx.get_node_attributes(G, 'label0').values())
                    and sorted(nx.get_edge_attributes(existing_G, 'label').values())
                    == sorted(nx.get_edge_attributes(G, 'label').values())
                ):
                    is_duplicate = True
                    break

            if not is_duplicate:
                graph_hashes[composite_key].add(graph_hash)
                unique_graphs.append([{ 'pattern_support': pattern_support, 'pattern_index': pattern_index, 'model_index': model_index }, G])

    return unique_graphs

def select_sublists(lst, pattern_indices):
    """
    Select specific sublists from a list based on pattern indices.

    :param lst: List of sublists.
    :param pattern_indices: List of pattern indices to select.
    :return: List of selected sublists.
    """
    selected_sublists = []
    for sublist in lst:
        if sublist[0]['pattern_index'] in pattern_indices:
            selected_sublists.append(sublist)
    return selected_sublists

# new_list = remove_duplicate_graphs(models_count)


def split_list_of_lists(input_list):
    """
    Split a list of lists into two separate lists.

    :param input_list: List of lists.
    :return: Two separate lists.
    """
    list_a = []
    list_b = []
    for sublist in input_list:
        list_a.append(sublist[0])
        list_b.append(sublist[1])
    return list_a, list_b

def check_and_clean_graphs(list0, list1):
    """
    Check and clean graphs based on a reference list.

    :param list0: Reference list of graphs.
    :param list1: List of graphs to check and clean.
    :return: List of cleaned graphs.
    """
    cleaned_list = []
    for item1 in list1:
        index_dict1, graph1 = item1
        pattern_index1 = index_dict1['pattern_index']

        for item0 in list0:
            index_dict0, graph0 = item0
            pattern_index0 = index_dict0['pattern_index']

            if pattern_index1 == pattern_index0:
                if nx.is_isomorphic(graph0, graph1): #node_match=lambda x, y: x['label'] == y['label']):
                    cleaned_list.append(item1)
                break

    return cleaned_list

from networkx.algorithms.isomorphism import GraphMatcher
def node_match(n1, n2):
    return n1.get('label') == n2.get('label')

def edge_match(e1, e2):
    return e1.get('label') == e2.get('label')

def remove_graphs_from_list(graph_list, graphs_to_remove):
    new_graph_list = []
    for [index_dict,target_graph] in graph_list:
        isomorphic = any(GraphMatcher(target_graph, G,
            node_match=node_match,
            edge_match=edge_match).is_isomorphic() for G in graphs_to_remove)
        if not isomorphic:
            new_graph_list.append([index_dict,target_graph])
    return new_graph_list

