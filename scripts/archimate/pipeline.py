import os, json
import archimate.transform
import archimate.filter
import utils.generateinput
from pathlib import Path

MODELS_DIR = './archimate/models/'
INPUT_DIR = './input/'

def import_models(directory: Path) -> list[dict]:
    models = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            file_path = os.path.join(MODELS_DIR, file)
            with open(file_path, encoding='utf-8') as f:
                models.append(json.load(f))
    return models

# utility function to see the structure of the created graphs
def print_graphs(graphs: list):
    for idx, graph in enumerate(graphs, start=1):
        nodes = list(graph.nodes)
        edges = list(graph.edges)
        for node in nodes:
            print(f"Node {node}: {graph.nodes[node]}")
        for edge in edges:
            print(f"Edge {edge}: {graph.edges[edge]}")

def start():
    # model import
    print(f"Importing models from directory '{MODELS_DIR}'...")
    models = import_models(MODELS_DIR)
    print(f"{len(models)} models imported.")

    # create and store graphs
    graphs = archimate.transform.create_graphs(models, INPUT_DIR)
    # print_graphs(graphs)

    # filters
    element_labels = archimate.filter.filter_element_types()
    relationship_labels = archimate.filter.filter_relationship_types()
    node_labels = element_labels + relationship_labels
    edge_labels = archimate.filter.filter_edge_labels()

    # re-create filtered graphs
    new_graphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
    new_graphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)

    # store re-created filtered graphs
    download_graphs = utils.generateinput.save_graphs_to_pickle(new_graphs, './input/archimate-graphs.pickle')
    data = utils.generateinput.graphs_to_data_file(new_graphs_with_names, 'archimate-graphs')

    # TODO: PlantUML visualization
