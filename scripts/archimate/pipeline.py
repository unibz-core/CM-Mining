import os, json
import sys
import archimate.transform
import archimate.filter
import utils.generateinput
from pathlib import Path
import timeout_decorator
import utils.command
import utils.gspanMiner

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
    try:
        # model import
        print(f"Importing models from directory '{MODELS_DIR}'...")
        models = import_models(MODELS_DIR)
        print(f"{len(models)} models imported.")

        # create and store graphs
        graphs = archimate.transform.create_graphs(models, INPUT_DIR)
        # print_graphs(graphs)

        # filters
        element_filter_kind = archimate.filter.select_element_filter_kind()
        element_labels = []
        if element_filter_kind == 'Specific Types':
            element_labels = archimate.filter.filter_element_types()
        elif element_filter_kind == 'Layers':
            element_labels = archimate.filter.filter_layers()
        elif element_filter_kind == 'Aspects':
            element_labels = archimate.filter.filter_aspects()
        else:
            # should not happen
            print("Error: Unsupported filter kind")
            sys.exit()
            
        relationship_labels = archimate.filter.filter_relationship_types()
        node_labels = element_labels + relationship_labels
        edge_labels = archimate.filter.filter_edge_labels()

        # re-create filtered graphs
        new_graphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
        new_graphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)

        # store re-created filtered graphs
        download_graphs = utils.generateinput.save_graphs_to_pickle(new_graphs, './input/graphs.pickle')
        data = utils.generateinput.graphs_to_data_file(new_graphs_with_names, 'graphs')

        # set parameters and run gSpan Miner
        gsParameters = utils.command.parameters()
        inputs = utils.gspanMiner.gsparameters(gsParameters)

        # Use timeout_decorator.timeout to handle function timeout
        @timeout_decorator.timeout(60)
        def run_gspan_with_timeout(inputs):
            return utils.gspanMiner.run_gspan(inputs)

        patterns = run_gspan_with_timeout(inputs)
        
    except timeout_decorator.timeout_decorator.TimeoutError:
        print("gSpan Miner execution timed out.")
        # handle the timeout error appropriately (e.g., logging, fallback, etc.)
    except Exception as e:
        print(f"Error: {e}")
        # handle other exceptions as needed

    # delete files
    utils.command.firststop()
    # TODO: PlantUML visualization