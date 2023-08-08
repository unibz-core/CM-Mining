# OntoUML2NetworkX

OntoUML2NetworkX is a Python library designed to facilitate the transformation of OntoUML models, represented in JSON files, into NetworkX graphs. This library provides a set of functions that enable the import of OntoUML data, generation of NetworkX graphs, and further processing of the resulting graphs. It offers a convenient way to work with OntoUML models within the NetworkX framework.

## Installation
You can install the library using the following pip command:

```bash
pip install ontouml2networkx
```

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

## Usage
Importing OntoUML Models and Generating NetworkX Graphs
To import OntoUML models from JSON files and generate NetworkX graphs, follow these steps:

Use the functions from the ontoumlimport module to extract class, generalization, and association information from JSON files.
Utilize the retrieved data to create NetworkX graphs representing the OntoUML model.
Leverage the power of NetworkX for graph analysis and visualization.

```python
import ontouml2networkx.ontoumlimport as oi

# Extract class and generalization information
classes = oi.get_classes(file_names)
generalizations = oi.get_generalizations(file_names)

# ... (more steps based on your specific use case)
```

Processing and Transforming NetworkX Graphs
The generateinput module offers functions for processing and modifying NetworkX graphs:

Use the provided functions to remove specific nodes and edges from NetworkX graphs based on labels.
Customize graph structures to focus on relevant information for your analysis.
```python
import ontouml2networkx.generateinput as gi

# Remove nodes with label "class" and edges with label "relation"
gi.remove_nodes_with_label(graph, "class")
gi.remove_edges_with_label(graph, "relation")

# ... (more processing and transformation steps)
```

## License
This project is licensed under the Apache License 2.0.

## Acknowledgments
You can use this section to credit any individuals, libraries, or resources that inspired or assisted your project.# CM-Mining