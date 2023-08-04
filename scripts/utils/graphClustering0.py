import networkx as nx

patternspath = "./input/outputpatterns.txt"

def convertPatterns(path):
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

def extract_features(graph_set):
    features = []
    
    for [index_dict,graph] in graph_set:
        index = index_dict['pattern_index']
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        node_labels = list(nx.get_node_attributes(graph, 'label').values())
        edge_labels = list(nx.get_edge_attributes(graph, 'label').values())
        
        features.append({
            'index': index,
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'node_labels': node_labels,
            'edge_labels': edge_labels
        })
    
    return features

import pandas as pd

def transform_graph_data(data):
    # Create an empty set to store all unique labels
    node_label_set = set()
    edge_label_set = set()

    # Iterate through the list to collect all unique labels
    for item in data:
        node_label_set.update(item['node_labels'])
        edge_label_set.update(item['edge_labels'])

    # Create an empty list to store the transformed data
    transformed_data = []

    # Iterate through the list again to populate the transformed data
    for item in data:
        row = {
            'index': item['index'],
            'num_nodes': item['num_nodes'],
            'num_edges': item['num_edges']
        }

        # Count the occurrence of node labels within the current graph
        for label in node_label_set:
            row[label] = item['node_labels'].count(label) if label in item['node_labels'] else 0

        # Count the occurrence of edge labels within the current graph
        for label in edge_label_set:
            row[label] = item['edge_labels'].count(label) if label in item['edge_labels'] else 0

        transformed_data.append(row)

    # Create the dataframe from the transformed data
    df = pd.DataFrame(transformed_data)

    # Fill missing values with 0 for the columns representing the absence of labels
    df = df.fillna(0)

    # Reorder the columns to match the desired column order
    desired_columns = ['index','num_nodes', 'num_edges'] + sorted(node_label_set) + sorted(edge_label_set)
    df = df[desired_columns]

    return df

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(df):
    # Compute the cosine similarity matrix
    similarity_matrix = cosine_similarity(df.values)

    # Convert the similarity matrix to a DataFrame
    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

    return similarity_df


import pandas as pd
from sklearn.cluster import KMeans

def group_similar_items(similarity_matrix, threshold):
    groups = []
    visited = set()

    # Iterate over each item in the similarity matrix
    for item in similarity_matrix.index:
        if item not in visited:
            # Create a new group for the item
            group = set()
            group.add(item)
            visited.add(item)

            # Find similar items above the threshold and add them to the group
            similar_items = similarity_matrix.index[similarity_matrix[item] >= threshold].tolist()
            for similar_item in similar_items:
                if similar_item not in visited:
                    group.add(similar_item)
                    visited.add(similar_item)

            groups.append(list(group))

    # Assign cluster labels to each item
    cluster_labels = ['cluster_{}'.format(i) for i in range(len(groups))]
    result = []
    for i, group in enumerate(groups):
        for item in group:
            result.append([item, cluster_labels[i]])

    return result

def merge_lists(list0, list1):
    return [
        [{**item1[0], 'pattern_cluster': item0[1][len('cluster_'): ]}, item1[1]]
        for item0, item1 in zip(list0, list1)
    ]
