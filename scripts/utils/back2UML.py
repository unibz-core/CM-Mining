"""
This module provides functions for processing and converting network graphs using the NetworkX library. 
Network graphs are represented as graph-pattern pairs, and the module includes two main functions: 
process_genset_cardinalities and convert_graphs_new.
"""

import networkx as nx

def get_unique_id(input_string):
    """
    Generate a unique identifier based on the input string.

    :param input_string: Input string to generate the unique identifier.
    :return: Unique identifier.
    """
    unique_id = hash(input_string)
    unique_id = abs(unique_id) % 100  # Limit the ID to a maximum of two digits
    letter = chr(ord('A') + (unique_id % 26))  # Map the ID to a letter (A-Z)
    return f"{letter}{unique_id:02d}"  # Format the ID with a leading zero if necessary

import networkx as nx

def process_genset_cardinalities(graphs):
    """
    Process graphs by copying edge labels to gen-set nodes and adding index to gen-set node labels.

    :param graphs: List of graph-pattern pairs.
    :return: List of processed graph-pattern pairs.
    """
    processed_graphs = []

    for [index_dict, G] in graphs:
        # Step 1: Copy edge labels to gen-set nodes
        for u, v, edge_data in list(G.edges(data=True)):
            if edge_data['label'] in ['isComplete', 'isDisjoint']:
                if G.nodes[u]['label'] == 'gen-set':
                    if 'label0' not in G.nodes[u]:
                        G.nodes[u]['label0'] = f"{edge_data['label']}{G.nodes[v]['label']}"
                    else:
                        G.nodes[u]['label0'] += f"_{edge_data['label']}{G.nodes[v]['label']}"
                elif G.nodes[v]['label'] == 'gen-set':
                    if 'label0' not in G.nodes[v]:
                        G.nodes[v]['label0'] = f"{edge_data['label']}{G.nodes[u]['label']}"
                    else:
                        G.nodes[v]['label0'] += f"_{edge_data['label']}{G.nodes[u]['label']}"

        nodes_to_remove = []
        for u, v, edge_data in list(G.edges(data=True)):
            if edge_data['label'] == 'cardinalities':
                if G.nodes[u]['label'] in ["characterization", "comparative", "externalDependence", "material",
                                           "mediation", "componentOf", "memberOf", "subCollectionOf", "subQuantityOf",
                                           "bringsAbout", "creation", "historicalDependence", "manifestation",
                                           "participation", "participational", "termination", "triggers",
                                           "instantiation", "relation"]:
                    if 'label0' not in G.nodes[u]:
                        G.nodes[u]['label0'] = f"{G.nodes[v]['label']}"
                        #G.remove_node(v)
                        nodes_to_remove.append(v)
                    else:
                        G.nodes[u]['label0'] += f"{G.nodes[v]['label']}"
                        #G.remove_node(v)
                        nodes_to_remove.append(v)
                elif G.nodes[v]['label'] in ["characterization", "comparative", "externalDependence", "material",
                                             "mediation", "componentOf", "memberOf", "subCollectionOf",
                                             "subQuantityOf", "bringsAbout", "creation", "historicalDependence",
                                             "manifestation", "participation", "participational", "termination",
                                             "triggers", "instantiation", "relation"]:
                    if 'label0' not in G.nodes[v]:
                        G.nodes[v]['label0'] = f"{G.nodes[u]['label']}"
                        #G.remove_node(u)
                        nodes_to_remove.append(u)
                    else:
                        G.nodes[v]['label0'] += f"{G.nodes[u]['label']}"
                        #G.remove_node(u)
                        nodes_to_remove.append(u)
        G.remove_nodes_from(nodes_to_remove)

        # Step 2: Add index to gen-set node labels
        gen_set_count = 0
        for node, node_data in G.nodes(data=True):
            if node_data['label'] == 'gen-set':
                if 'label0' in node_data:
                    # Skip if label0 already exists
                    #node_data['label0'] += f"{node_data.get('label0', '')}"
                    continue
                node_data['label0'] = f"{gen_set_count}_{node_data.get('label0', '')}"
                gen_set_count += 1
        
        for u, v, edge_data in G.edges(data=True):
            if edge_data['label'] == 'generalization':
                if G.nodes[u]['label'] == 'gen' and G.nodes[v]['label'] == 'gen-set':
                    if 'label0' in G.nodes[v]:
                        G.nodes[u]['label0'] = G.nodes[v]['label0']
                if G.nodes[v]['label'] == 'gen' and G.nodes[u]['label'] == 'gen-set':
                    if 'label0' in G.nodes[u]:
                        G.nodes[v]['label0'] = G.nodes[u]['label0']
        
        # Step 4: Remove nodes with specific labels
        labels_to_remove = ['gen-set', 'True', 'False']
        nodes_to_remove = [node for node, node_data in list(G.nodes(data=True)) if node_data['label'] in labels_to_remove]

        # Create a copy of the graph and remove nodes from the copy
        G_copy = G.copy()
        G_copy.remove_nodes_from(nodes_to_remove)

        processed_graphs.append([index_dict, G_copy])

    return processed_graphs


def convert_graphs_new(graphs):
    """
    Convert graphs by modifying single edges and adding new nodes.

    :param graphs: List of graph-pattern pairs.
    :return: List of converted graph-pattern pairs.
    """
    converted_graphs = []
    for [index_dict,G] in graphs:
        # create a new directed graph
        H = nx.DiGraph()

        # modify remaining single edges in the input graph
        for n0, n1, attr in list(G.edges(data=True)):
            label_ = attr['label']
            if label_ in ["restrictedTo"]:
                H.add_edge(n0, n1, label="restrictedto")
            elif label_ in ["source", "target", "general", "specific"]:
                if label_ == "general":
                    if G.nodes[n1]['label'] == "gen":
                        node2 = f"Class{n1}"
                        H.add_node(node2, label="class")
                        #H.add_edge(node2, n0, label="gen")
                        H.add_edge(node2, n0, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0']) if 'label0' in G.nodes[n1] else H.add_edge(node2, n0, label=G.nodes[n1]['label'])
                    if G.nodes[n0]['label'] == "gen":
                        node2 = f"Class{n0}"
                        H.add_node(node2, label="class")
                        #H.add_edge(node2, n1, label="gen")
                        H.add_edge(node2, n1, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0']) if 'label0' in G.nodes[n0] else H.add_edge(node2, n1, label=G.nodes[n0]['label'])
                if label_ == "specific":
                    if G.nodes[n1]['label'] == "gen":
                        node2 = f"Class{n1}"
                        H.add_node(node2, label="class")
                        #H.add_edge(n0,node2, label="gen")
                        H.add_edge(n0,node2, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0']) if 'label0' in G.nodes[n1] else H.add_edge(n0,node2, label=G.nodes[n1]['label'])
                    if G.nodes[n0]['label'] == "gen":
                        node2 = f"Class{n0}"
                        H.add_node(node2, label="class")
                        #H.add_edge(n1,node2, label="gen")
                        H.add_edge(n1,node2, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0']) if 'label0' in G.nodes[n0] else H.add_edge(n1,node2, label=G.nodes[n0]['label'])
                if label_ == "target":
                    if G.nodes[n1]['label'] in ["characterization", "comparative", "externalDependence", "material", "mediation", "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout", "creation", "historicalDependence", "manifestation", "participation", "participational", "termination", "triggers", "instantiation", "relation"]:
                        node2 = f"Class{n1}"
                        H.add_node(node2, label="class")
                        #H.add_edge(n0, node2, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0']) 
                        H.add_edge(n0, node2, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0']) if 'label0' in G.nodes[n1] else H.add_edge(n0, node2, label=G.nodes[n1]['label'])   
                    if G.nodes[n0]['label'] in ["characterization", "comparative", "externalDependence", "material", "mediation", "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout", "creation", "historicalDependence", "manifestation", "participation", "participational", "termination", "triggers", "instantiation", "relation"]:
                        node2 = f"Class{n0}"
                        H.add_node(node2, label="class")
                        #H.add_edge(n1, node2, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0'])
                        H.add_edge(n1, node2, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0']) if 'label0' in G.nodes[n0] else H.add_edge(n1, node2, label=G.nodes[n0]['label'])   
                if label_ == "source":
                    if G.nodes[n1]['label'] in ["characterization", "comparative", "externalDependence", "material", "mediation", "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout", "creation", "historicalDependence", "manifestation", "participation", "participational", "termination", "triggers", "instantiation", "relation"]:
                        node2 = f"Class{n1}"
                        H.add_node(node2, label="class")
                        #H.add_edge(node2, n0, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0'])
                        H.add_edge(node2, n0, label=G.nodes[n1]['label'], label0=G.nodes[n1]['label0']) if 'label0' in G.nodes[n1] else H.add_edge(node2, n0, label=G.nodes[n1]['label'])
                    if G.nodes[n0]['label'] in ["characterization", "comparative", "externalDependence", "material", "mediation", "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout", "creation", "historicalDependence", "manifestation", "participation", "participational", "termination", "triggers", "instantiation", "relation"]:
                        node2 = f"Class{n0}"
                        H.add_node(node2, label="class")
                        #H.add_edge(node2, n1, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0'])
                        H.add_edge(node2, n1, label=G.nodes[n0]['label'], label0=G.nodes[n0]['label0']) if 'label0' in G.nodes[n0] else H.add_edge(node2, n1, label=G.nodes[n0]['label'])   
        
        for n, attr in list(G.nodes(data=True)):
            label = attr.get('label')
            label0 = attr.get('label0')
            H.add_node(n, label=label, label0=label0)
        
        for n0, n1 in list(H.edges):
            if H.has_node(n1):
                for n2 in list(H.neighbors(n1)):
                    if n0 in H and n1 in H and n2 in H:
                        if (H.has_edge(n0, n1) and H.has_edge(n1, n2) and H.nodes[n1]['label'] == "class"):
                            label_n0_n1 = H.edges[(n0, n1)]['label']
                            label0_n0_n1 = H.edges[(n0, n1)].get('label0', '')
                            H.add_edge(n0, n2, label=label_n0_n1, label0=label0_n0_n1)
                            H.remove_node(n1)

        converted_graphs.append([index_dict,H])

    return converted_graphs
