import pandas as pd
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

def graph_to_dataframe(G):
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

G = nx.Graph()
G.add_edge("n1", "n0", label="specific")
G.add_edge("n2", "n0", label="general")
G.add_node("n0", label="gen")
G.add_node("n1", label="subkind")
G.add_node("n2", label="kind")
G.add_edge("n1", "n3", label="source")
G.add_edge("n3", "n4", label="target")
G.add_node("n3", label="material")
G.add_node("n4", label="role")

def dataframe2vector(df):
    vector = []
    for index, row in df.iterrows():
        for column, value in row.items():  # Replace iteritems() with items()
            vector.append((index, column, value))
    return vector

def graphs2dataframes2vectors(graph_list):
    # Convert each graph in the list to a DataFrame
    vectors = []
    for index_dict,G in graph_list:
        #index = index_dict['pattern_index']
        df = graph_to_dataframe(G)
        vector = index_dict,dataframe2vector(df)
        vectors.append(vector)
    return vectors


def transform2singledataframe(input_list):
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

from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(df):
    # Compute the cosine similarity matrix
    similarity_matrix = cosine_similarity(df.values)

    # Convert the similarity matrix to a DataFrame
    similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)

    return similarity_df

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

# pattern_graphs = convertPatterns(patternspath)
# list_of_vectors = graphs2dataframes2vectors(pattern_graphs)
# singledtaframe = transform2singledataframe(list_of_vectors)
# patterns_similarity_matrix = calculate_similarity(singledtaframe)
# grouped_items = group_similar_items(patterns_similarity_matrix,0.4)
# print(singledtaframe)
# print(patterns_similarity_matrix)
# print(grouped_items)







#test = list_of_dataframes[5]
# print(list_of_dataframes)


# Given networkx graph G


# Convert the graph to a pandas DataFrame
#df = graph_to_dataframe(G)
#print(df)




#     n1  n0  n2  n3  n4  kind  subkind  gen  material  role
# n1   0   1   0   1   0    0         2    0         0     0
# n0   1   0   1   0   0    0         0    2         0     0
# n2   0   1   0   0   0    2         0    0         0     0
# n3   1   0   0   0   1    0         0    0         2     0
# n4   0   0   0   1   0    0         0    0         0     2   

#     n1  n0  n2  n3  n4  kind  subkind  gen  material  role
# n1   0   2   0   2   0     0        2    0         0     0
# n0   2   0   2   0   0     0        0    2         0     0
# n2   0   2   0   0   0     2        0    0         0     0
# n3   2   0   0   0   2     0        0    0         2     0
# n4   0   0   0   2   0     0        0    0         0     2
