"""
This Python module is an alternative option of graphCLustering0.py and provides functions for processing 
and analyzing patterns represented as NetworkX graphs. It includes functionality for converting patterns from a file into NetworkX graph format,
extracting features from graph patterns, transforming data for analysis, calculating pairwise cosine similarity between graphs, grouping similar items based on similarity, 
and merging data with additional information
"""

import pandas as pd
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity

patternspath = "./input/outputpatterns.txt"

def convertPatterns(path):
    """
    Convert patterns from a file to a list of NetworkX graphs.

    :param path: Path to the file containing patterns.
    :return: List of NetworkX graphs representing the patterns.
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

def graph2dataframe(G):
    """
    Convert a NetworkX graph to a DataFrame representing node connections, labels, and edges.

    :param G: NetworkX graph to be converted.
    :return: DataFrame representation of the graph.
    """
    # Get a list of all nodes and node labels in the graph
    nodes = list(G.nodes())
    node_labels = {node: G.nodes[node].get("label", 0) for node in nodes}
    label_columns = sorted(set(node_labels.values()) - {0})
    
    # Initialize an empty DataFrame with all nodes and label columns
    columns = nodes + label_columns
    df = pd.DataFrame(0, columns=columns, index=nodes)
    
    # Fill the DataFrame with node connections (1), "specific" connections (1), and "general" connections (-1)
    for node in nodes:
        for neighbor in G.neighbors(node):
            edge_label = G.get_edge_data(node, neighbor).get("label", None)
            if edge_label == "specific":
                df.at[node, neighbor] = -1
            elif edge_label == "source":
                df.at[node, neighbor] = -2
            elif edge_label == "general":
                df.at[node, neighbor] = 1
            elif edge_label == "target":
                df.at[node, neighbor] = 2
            else:
                df.at[node, neighbor] = 1
 
    # Fill the DataFrame with node labels (2)
    for node in nodes:
        label = node_labels[node]
        df.at[node, label] = 3
            
    return df


def dataframe2vector(df):
    """
    Convert a DataFrame representation of a graph to a vector format.

    :param df: DataFrame representing a graph.
    :return: Vectorized representation of the graph.
    """
    vector = []
    for index, row in df.iterrows():
        for column, value in row.items():  # Replace iteritems() with items()
            vector.append((index, column, value))
    return vector

def graphs2dataframes2vectors(graph_list):
    """
    Convert a list of graph-pattern pairs to a list of vectorized data.

    :param graph_list: List of graph-pattern pairs.
    :return: List of vectorized data.
    """
    # Convert each graph in the list to a DataFrame
    vectors = []
    for index_dict,G in graph_list:
        #index = index_dict['pattern_index']
        df = graph2dataframe(G)
        vector = index_dict,dataframe2vector(df)
        vectors.append(vector)
    return vectors


def transform2singledataframe(input_list):
    """
    Transform a list of data into a single DataFrame.

    :param input_list: List of tuples containing pattern data and tuple lists.
    :return: Transformed DataFrame.
    """
    # Initialize an empty list to store dictionaries containing data for each row
    data_list = []
    
    # Initialize the columns list to store column names
    columns = []

    # Iterate over the list of tuples
    for idx, (pattern_dict, tuple_list) in enumerate(input_list):
        pattern_index = pattern_dict['pattern_index']

        # Initialize a dictionary to store the values for the current row
        row_data = {}

        # Iterate over the tuples in the list and populate the row_data dictionary
        for tpl in tuple_list:
            tpl_str = str(tpl)  # Convert the tuple to a string to use it as a key
            row_data[tpl_str] = 1

            # Add the column name to the columns list if it's not already there
            if tpl_str not in columns:
                columns.append(tpl_str)

        # Add the row data to the data_list
        data_list.append(row_data)

    # Create a DataFrame from the data_list
    df = pd.DataFrame(data_list)

    # Sort the columns in a specific order
    df = df.reindex(sorted(columns), axis=1)

    # Fill NaN values with 0
    df = df.fillna(0)

    return df

def calculate_similarity(df):
    """
    Calculate cosine similarity between vectors in a DataFrame.

    :param df: DataFrame containing vectors.
    :return: DataFrame of cosine similarity scores.
    """
    # Compute the cosine similarity matrix
    similarity_matrix = cosine_similarity(df.values)

    # Convert the similarity matrix to a DataFrame
    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

    return similarity_df

def group_similar_items(similarity_matrix, threshold):
    """
    Group similar items based on cosine similarity and a threshold.

    :param similarity_matrix: DataFrame of cosine similarity scores.
    :param threshold: Similarity threshold for grouping.
    :return: List of grouped items.
    """
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
    """
    Merge two lists of data with additional information.

    :param list0: List of pattern-cluster pairs.
    :param list1: List of graph-pattern pairs.
    :return: Merged list with pattern-cluster information.
    """
    return [
        [{**item1[0], 'pattern_cluster': item0[1][len('cluster_'): ]}, item1[1]]
        for item0, item1 in zip(list0, list1)
    ]






