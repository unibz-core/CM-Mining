# Conceptual Models Pattern Mining and Analysis Toolkit

The Conceptual Models Pattern Mining and Analysis Toolkit provides a collection of Python modules for processing, analyzing, and visualizing graph patterns from OntoUML data. It's designed to help you to analyze OntoUML models, extract patterns, calculate frequencies, find subgraph isomorphisms, and generate visual representations of your mining output.

## Table of Contents

- [Installation](#installation)
- [Modules](#modules)
- [Usage](#usage)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation
You can install the library using the following pip command:

```bash
git clone https://github.com/unibz-core/CM-Mining
```

- create the following folders, `domain_patterns`, `patterns`, `input`.
- install the dependencies you find in the `requirements.txt` file.
- run the `main.py` file from the root `script` folder. 
- (!) Note that this application requires `Python==3.9`

## Modules

### ontoumlimport.py

The ontoumlimport module is responsible for importing OntoUML data from JSON files and generating NetworkX graphs based on the imported data. It contains functions that allow you to extract class, generalization, and association information from the JSON files and create corresponding NetworkX graph structures.

Functions:
- `get_classes(x)`: Extracts class information from JSON files and returns a structured representation.
- `get_generalizations(x)`: Retrieves generalization relationships from JSON files and organizes them for graph creation.
- `get_associations(x)`: Collects association details from JSON files and prepares them for inclusion in the NetworkX graph.
- `get_genset(x)`: Gathers information about generalization sets and their components from JSON files.
- `get_restrictedTo(x)`: Retrieves the "restricted to" information for classes from JSON files.
- `pairwise(iterable)`: Iterates through pairs of items in an iterable.
- `get_genset_rel(x)`: Generates relationships for generalization sets and their components.
- `create_FullUndirectedGraphs(...)`: Creates NetworkX graphs with nodes and edges from imported OntoUML data.

### generateinput.py

The generateinput module offers functions for processing and transforming NetworkX graphs generated from OntoUML data. It provides methods to remove specific nodes and edges based on labels, facilitating the customization of graph structures. These functions enable you to create specialized graph views based on your analysis needs.

Functions
- `remove_nodes_with_label(graph, label)`: Removes nodes with a specified label from the given graph.
- `remove_edges_with_label(graph, label)`: Deletes edges with a specified label from the given graph.
- `process_graphs(node_labels, edge_labels, graphs)`: Processes NetworkX graphs by removing nodes and edges based on labels.
- `process_graphs_with_names(node_labels, edge_labels, graphs)`: Processes graphs while retaining their names.
- `process_graphs_(node_labels, edge_labels, graphs)`: Processes graphs with additional support and index information.
- `process_graphs__(node_labels, edge_labels, graphs)`: Processes graphs with index dictionary information.
- `replace_labels_with_default(class_labels, relation_labels, edge_labels, graphs)`: Replaces labels in graphs with default class and relation labels.
- `save_graphs_to_pickle(graphs, filename)`: Saves a list of NetworkX graphs to a pickle file.
- `flatten(lst)`: Flattens a nested list.
- `graphs_to_data_file(graphs, name)`: Writes NetworkX graphs to a data file in a specific format.

### command.py

This Python module provides command-line interface functionalities for interacting with UML diagrams and patterns. It facilitates various operations related to UML diagrams, including:

Functions
- `filterClasses()`: Prompt the user to select classes to filter out from UML diagrams.
- `filterRelations()`: Prompt the user to select relations to filter out from UML diagrams.
- `filterEdges()`: Prompt the user to select edges to filter out from UML diagrams.
- `parameters()`: Prompt the user to enter parameters, such as minimum support and minimum number of vertices.
- `process_pattern()`: Process patterns and perform various operations on them.
- `viz_uml_diagrams()`: Visualize UML diagrams using PlantUML.

Flexible Process Control:
- `firststop()`: Prompt the user to stop the process or proceed to the next function.
- `secondstop()`: Prompt the user to stop the process or proceed to the next function.
- `laststop()`: Prompt the user to delete files or proceed to the next function.

### gspanMiner.py

This Python module provides functions related to running the gSpan algorithm for graph mining.

Functions
- `run_gspan(input)`: Run the gSpan algorithm with a specified input configuration.
- `gsparameters(values)`: Generate gSpan algorithm parameters based on input values.

### graphClustering0.py

This Python module provides functions for processing, clustering and analyzing patterns represented as NetworkX graphs. 

Functions
- `convertPatterns(path)`: Convert patterns from a file into NetworkX graph format.
- `extract_features(graph_set)`: Extract features from a set of graphs.
- `transform_graph_data(data)`: Transform graph data into a DataFrame suitable for analysis.
- `calculate_similarity(df)`: Calculate pairwise cosine similarity between graphs.
- `group_similar_items(similarity_matrix, threshold)`: Group similar items based on cosine similarity and a threshold.
- `merge_lists(list0, list1)`: Merge two lists of data with additional information.

### graphClustering1.py

This Python module is an alternative option to the graphCLustering0.py module and provides functions for processing and analyzing patterns represented as NetworkX graphs. 

Functions
- `convertPatterns(path)`: Convert patterns from a file into a list of NetworkX graphs.
- `graph2dataframe(G)`: Convert a NetworkX graph to a DataFrame representing node connections, labels, and edges.
- `dataframe2vector(df)`: Convert a DataFrame representation of a graph to a vector format.
- `graphs2dataframes2vectors(graph_list)`: Convert a list of graph-pattern pairs to a list of vectorized data.
- `transform2singledataframe(input_list)`: Transform a list of data into a single DataFrame.
- `calculate_similarity(df)`: Calculate cosine similarity between vectors in a DataFrame.
- `group_similar_items(similarity_matrix, threshold)`: Group similar items based on cosine similarity and a threshold.
- `merge_lists(list0, list1)`: Merge two lists of data with additional information.

### patterns.py

This Python module provides functions related to processing the patterns:

Functions
- `load_graphs_from_pickle(filename)`: Load a list of NetworkX graphs from a pickle file.
- `convertPatterns(path)`: Convert patterns from a file into NetworkX graphs.
- `return_all_domain_info(graphs)`: Return domain information for each graph.
- `count_subgraph_isomorphisms(source_graphs, target_graphs)`: Count subgraph isomorphisms between source and target graphs.
- `remove_duplicate_graphs(graphs)`: Remove duplicate graphs from a list of graphs.
- `select_sublists(lst, pattern_indices)`: Select specific sublists from a list based on pattern indices.
- `split_list_of_lists(input_list)`: Split a list of lists into two separate lists.
- `check_and_clean_graphs(list0, list1)`: Check and clean graphs based on a reference list.

### back2UML.py

This module provides functions for processing and converting network graphs using the NetworkX library. Network graphs are represented as graph-pattern pairs, and the module includes two main functions: process_genset_cardinalities and convert_graphs_new.

Functions
- `get_unique_id(input_string)`: Generate a unique identifier based on the input string.
- `process_genset_cardinalities(graphs)`: Process graphs by copying edge labels to gen-set nodes and adding an index to gen-set node labels.
- `convert_graphs_new(graphs)`: Convert graphs by modifying single edges and adding new nodes.

### UMLviz.py

This Python module provides functions for converting a list of NetworkX graphs into PlantUML diagrams for different purposes.

Functions
- `convert_to_plantuml_domain(graphs, title="Caption", output_folder="domain_patterns")`: Converts a list of network graphs into PlantUML diagrams for individual domains.
- `convert_to_plantuml_clusters(graphs, title="Caption", output_folder="patterns")`: Converts a list of network graphs into PlantUML diagrams for patterns within clusters.

### plantumlGenerator.jar

Check this [page](https://plantuml.com/download)

## Usage

Follow the input from the command line and play. 

## License

This project is licensed under the Apache License 2.0.

## Acknowledgments

You can use this section to credit any individuals, libraries, or resources that inspired or assisted your project.# CM-Mining