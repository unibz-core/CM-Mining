import glob
import json
import jsonpath_rw_ext as jp
from itertools import chain
from functools import reduce

import os

directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension

# loop through the directory and get file names with the desired extension
file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)

#print(file_names)


# %%

def get_classes(x):
    class_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        class_name = jp.match('$..contents[?(@.type=="Class")].name', data)
        stereotype_name = jp.match('$..contents[?(@.type=="Class")].stereotype', data)
        id = jp.match('$..contents[?(@.type=="Class")].id', data)
        zipped = list(zip(id,stereotype_name,class_name))
        class_output.append(zipped)
    return class_output

def get_generalizations(x):
    gen_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        gen = jp.match('$..general.id', data)
        spec = jp.match('$..specific.id', data)
        genID = jp.match('$..contents[?(@.type=="Generalization")].id', data)
        zipped = list(zip(genID,gen,spec))
        gen_output.append(zipped)
    return gen_output

def get_associations(x):
    association_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        association_name = jp.match('$..contents[?(@.type=="Relation")].name', data)
        stereotype_name = jp.match('$..contents[?(@.type=="Relation")].stereotype', data)
        id = jp.match('$..contents[?(@.type=="Relation")].id', data)
        cardinalities = [item for item in jp.match('$..properties[?(@.cardinality)].cardinality', data) if item is not None]
        coupled_cardinalities = [cardinalities[n:n+2] for n in range(0, len(cardinalities), 2)]
        source_target0 = [item for item in jp.match('$..contents[?(@.type=="Relation")]', data) if item is not None]
        source_target1 = jp.match('$..propertyType.id', source_target0)
        coupled_source_target = [source_target1[n:n+2] for n in range(0, len(source_target1), 2)]
        zipped = [(a,str(b),str(c),d,*e) for a,b,c,d,e in zip(id,association_name,stereotype_name,coupled_cardinalities,coupled_source_target)]
        association_output.append(zipped)
    return association_output

def get_genset(x):
    gen_set_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        id = jp.match('$..contents[?(@.type=="GeneralizationSet")].id', data)
        disj = jp.match('$..contents[?(@.type=="GeneralizationSet")].isDisjoint', data)
        comp = jp.match('$..contents[?(@.type=="GeneralizationSet")].isComplete', data)
        name = jp.match('$..contents[?(@.type=="GeneralizationSet")].name', data)
        gen_ids = [jp.match('$..generalizations[?(@.id)].id', i) for i in jp.match('$..contents[?(@.type=="GeneralizationSet")]', data)]
        #zipped = [(a,'isComplete:'+str(b),'isDisjoint:'+str(c),str(d),*e) for a,b,c,d,e in zip(id,disj,comp,name,gen_ids)] unfold set of ids
        zipped = [(a,str(b),str(c),str(d),e) for a,b,c,d,e in zip(id,disj,comp,name,gen_ids)]
        gen_set_output.append(zipped)
    return gen_set_output

from itertools import combinations
#https://www.geeksforgeeks.org/python-all-possible-pairs-in-list/
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_genset_rel(x):
    list_ = []
    for i in x:
        gens = [(a,*e) for a,b,c,d,e in i]
        result = [list(map(lambda x: (i[0], x[1]), pairwise(i))) for i in gens]
        list_.append(result)
    return list_

# %%

classes_v = get_classes(file_names)

generalizations = get_generalizations(file_names)
generalizations_v = [[(a, "gen") for a,b,c in i] for i in generalizations]
generalizations_general = [[(b, a, "general") for a,b,c in i] for i in generalizations]
generalizations_specific = [[(c, a, "specific") for a,b,c in i] for i in generalizations]


associations = get_associations(file_names)
associations_v = [[(a, c, b) for a,b,c,d,e,f in i] for i in associations]

genset = get_genset(file_names)
genset_rel = [sum(i, []) for i in get_genset_rel(genset)]
# print(genset)
# print(genset_rel)

import networkx as nx

def create_graphs(file_names, nodesA, nodesB, nodesC, edgesA, edgesB):
    """
    Create a list of networkx graphs from lists of node and edge data.

    Parameters:
    file_names (list): A list of file names corresponding to the node and edge data.
    nodesA (list): A list of lists of node data, where each node is a tuple with one or more labels.
    nodesB (list): A list of lists of node data, where each node is a tuple with one or more labels.
    edgesA (list): A list of lists of edge data, where each edge is a tuple with one or more labels.
    edgesB (list): A list of lists of edge data, where each edge is a tuple with one or more labels.

    Returns:
    A list of networkx graph objects.
    """
    graphs = []

    for file_name, node_list_A, node_list_B, node_list_C, edge_list_A, edge_list_B in zip(file_names, nodesA, nodesB, nodesC, edgesA, edgesB):
        # Create an empty graph
        G = nx.Graph()

        # Add nodes to the graph
        for node_data in node_list_A:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_B:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_C:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)

        # Add edges to the graph
        for edge_data in edge_list_A:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_B:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)

        graphs.append(G)

    return graphs


graphs = create_graphs(file_names, classes_v, generalizations_v, associations_v, generalizations_general, generalizations_specific)

# Print nodes and edges for each graph
# for i, G in enumerate(graphs):
#     print(f"Graph {i+1}:")
#     print("Nodes:", G.nodes(data=True))
#     print("Edges:", G.edges(data=True))
#     print()

fd = open("output.txt", "r+")
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

out = [[k for k in w if 'Support:' not in k] for w in res]
out0 = [[k for k in w if 't #' not in k] for w in out]
out1 = [[k for k in w if 'Read:' not in k] for w in out0]
out2 = [[k for k in w if 'Mine:' not in k] for w in out1]
out3 = [[k for k in w if 'Total:' not in k] for w in out2]
out4 = [[s for s in sub_list if s] for sub_list in out3]
final_list = list(filter(None, out4))
#print("Resultant patterns list after grouping : " + str(final_list))
#print(final_list)

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
    # Append the graph to the list of graphs
    pattern_graphs.append(G)


import networkx as nx
from grandiso import find_motifs

def count_subgraph_isomorphisms(source_graphs, target_graphs):
    # Initialize a list to store the matched graphs for each match
    matches_list = []
    # Loop through each source graph and target graph
    for i, source_graph in enumerate(source_graphs):
        for j, target_graph in enumerate(target_graphs):
            # Use find_motifs to find matches
            matches = find_motifs(source_graph, target_graph) #directed=True)
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
                matched_dict = {'source_graph_index': i, 'target_graph_index': j, 'matched_graph': matched_graph, 'nodes': nodes, 'node_labels': node_labels, 'edge_labels': edge_labels}
                matches_list.append(matched_dict)
    return matches_list

H = nx.Graph()
H.add_node("n0", label="gen")
H.add_node("n1", label="kind")
H.add_node("n2", label="gen")
H.add_edge("n0", "n1", label="general")
H.add_edge("n1", "n2", label="general")

models_count = count_subgraph_isomorphisms([H],graphs)
for i in models_count:
    print(i)


# # Example usage
# file_names = ['graph1.txt', 'graph2.txt']
# nodesA = [[(1, 'A', 'B'), (2, 'C', 'D'), (3, 'E', 'F')], [(1, 'G', 'H'), (2, 'I', 'J'), (3, 'K', 'L')]]
# nodesB = [[(4, 'M', 'N'), (5, 'O', 'P')], [(4, 'Q', 'R'), (5, 'S', 'T')]]
# edgesA = [[(1, 2, 'X', 'Y'), (2, 3, 'Z', 'W')], [(1, 3, 'M', 'N'), (2, 3, 'O', 'P')]]
# edgesB = [[(4, 5, 'U', 'V')], [(4, 5, 'W', 'X')]]

# graphs = create_graphs(file_names, nodesA, nodesB, edgesA, edgesB)

# # Print nodes and edges for each graph
# for i, G in enumerate(graphs):
#     print(f"Graph {i+1}:")
#     print("Nodes:", G.nodes(data=True))
#     print("Edges:", G.edges(data=True))
#     print()


