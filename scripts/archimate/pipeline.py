import os, json
import subprocess
import archimate.transform
import archimate.filter
import archimate.visualization
import utils.generateinput
import timeout_decorator
import utils.command
import utils.gspanMiner
import utils.graphClustering1
import networkx as nx
from pathlib import Path

MODELS_DIR = './archimate/models/'
INPUT_DIR = './input/'
PATTERNS_FILE = './input/outputpatterns.txt'
PATTERNS_DIR = './patterns/'
PLANTUML_JAR_PATH = "./utils/plantumlGenerator.jar"

def import_models(directory: Path) -> list[dict]:
    models = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            file_path = os.path.join(MODELS_DIR, file)
            with open(file_path, encoding='utf-8') as f:
                models.append(json.load(f))
    return models

def print_graph(graph: nx.Graph):
    nodes = list(graph.nodes)
    edges = list(graph.edges)
    for node in nodes:
        print(f"Node {node}: {graph.nodes[node]}")
    for edge in edges:
        print(f"Edge {edge}: {graph.edges[edge]}")

# utility function to see the structure of the created graphs
def print_graphs(graphs: list[nx.Graph]):
    for idx, graph in enumerate(graphs, start=1):
        print_graph(graph)

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
        
        relationship_labels = archimate.filter.filter_relationship_types()
        node_labels = element_labels + relationship_labels
        edge_labels = archimate.filter.filter_edge_labels()

        # re-create filtered graphs
        new_graphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
        new_graphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)

        # store re-created filtered graphs
        utils.generateinput.save_graphs_to_pickle(new_graphs, './input/graphs.pickle')
        utils.generateinput.graphs_to_data_file(new_graphs_with_names, 'graphs')

        # set parameters gspan parameters
        gsParameters = utils.command.parameters()
        inputs = utils.gspanMiner.gsparameters(gsParameters)

        # use timeout_decorator.timeout to handle function timeout
        @timeout_decorator.timeout(60)
        def run_gspan_with_timeout(inputs):
            return utils.gspanMiner.run_gspan(inputs)
        
        # run gspan Miner
        run_gspan_with_timeout(inputs)

    except timeout_decorator.timeout_decorator.TimeoutError:
        print("gSpan Miner execution timed out.")
        # handle the timeout error appropriately (e.g., logging, fallback, etc.)
    except Exception as e:
        print(f"Error: {e}")
        # handle other exceptions as needed

    utils.command.firststop()

    pattern_graphs = utils.patterns.convertPatterns(PATTERNS_FILE)

    # todo? filter known patterns

    # clustering
    patterns_features = utils.graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    patterns_dataframe = utils.graphClustering1.transform2singledataframe(patterns_features)
    patterns_similarity_matrix = utils.graphClustering1.calculate_similarity(patterns_dataframe)
    similarity_threshold = utils.command.ask_similarity_threshold()
    patterns_cluster_labels = utils.graphClustering1.group_similar_items(patterns_similarity_matrix, similarity_threshold)
    pattern_graphs_clustered = utils.graphClustering1.merge_lists(patterns_cluster_labels, pattern_graphs)

    # create plantUML diagram text file for each pattern
    for pattern in pattern_graphs_clustered:
        # file path: ./patterns/<cluster>/<pattern_support>_<pattern_index>.txt
        p_cluster_dir = os.path.join(PATTERNS_DIR, pattern[0]['pattern_cluster'])
        if not os.path.exists(p_cluster_dir):
            os.mkdir(p_cluster_dir)
        pattern_file = os.path.join(p_cluster_dir, f"{pattern[0]['pattern_support']}_{pattern[0]['pattern_index']}.txt")
        
        # bring pattern graph into standard graph structure 
        cleaned_pattern_graph = archimate.transform.clean_graph(pattern[1])
        archimate.visualization.generate_diagram(cleaned_pattern_graph[0], cleaned_pattern_graph[1], pattern_file)

    generated_files = Path(PATTERNS_DIR).glob('**/*.txt')

    # limit number of files to generate images for (since this can take very long for a large amount of files)
    max_diagram_amount = archimate.filter.input_max_diagram_amount()
    
    # generate diagram images using the plantUML jar
    for idx, txt_file in enumerate(generated_files, start=0):
        if idx >= max_diagram_amount:
            break
        
        cmd = f"java -jar {PLANTUML_JAR_PATH} {txt_file}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Generated diagram for: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not generate diagram for {txt_file.name}: {e}")