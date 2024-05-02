import os, json
import subprocess
import warnings
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
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn

MODELS_DIR = './archimate/models/'
INPUT_DIR = './input/'
PICKLE_FILE = './input/graphs.pickle'
PATTERNS_FILE = './input/outputpatterns.txt'
PATTERNS_DIR = './patterns/'
PLANTUML_JAR_PATH = "./utils/plantumlGenerator.jar"
MINING_DURATION = 60

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


def step1():
    '''
    - Import models
    - Create networkX graphs
    - Filter elements/relationships
    - Run gspan miner
    '''
    # model import
    print(f"Importing models from directory '{MODELS_DIR}'...")
    models = import_models(MODELS_DIR)
    print(f"Imported {len(models)} models.\n")

    # create networkX graphs
    graphs = archimate.transform.create_graphs(models, INPUT_DIR)
    
    # filter elements (by type/layer/aspect)
    element_filter_kind = archimate.filter.select_element_filter_kind()
    element_labels = []
    if element_filter_kind == 'Specific Types':
        element_labels = archimate.filter.filter_element_types()
    elif element_filter_kind == 'Layers':
        element_labels = archimate.filter.filter_layers()
    elif element_filter_kind == 'Aspects':
        element_labels = archimate.filter.filter_aspects()

    # filter relationships
    relationship_labels = archimate.filter.filter_relationship_types()
    node_labels = element_labels + relationship_labels
    edge_labels = archimate.filter.filter_edge_labels()

    # re-create filtered graphs
    new_graphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
    new_graphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)

    # store re-created filtered graphs
    utils.generateinput.save_graphs_to_pickle(new_graphs, PICKLE_FILE)
    print(f"\nFiltered graph stored in file: '{PICKLE_FILE}'.")
    utils.generateinput.graphs_to_data_file(new_graphs_with_names, 'graphs')
    print("Filtered graph stored in file: [green]'./input/graphs.data'[/green].\n")

    # set gspan parameters
    gspan_params = utils.command.parameters()
    inputs = utils.gspanMiner.gsparameters(gspan_params)

    # use timeout_decorator.timeout to handle function timeout
    @timeout_decorator.timeout(MINING_DURATION)
    def run_gspan_with_timeout(inputs):
        return utils.gspanMiner.run_gspan(inputs)

    with Progress(
        SpinnerColumn(spinner_name='point'),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        redirect_stdout=False,
        redirect_stderr=False
    ) as progress:
        progress.add_task(
            description=f"Mining patterns... ({MINING_DURATION} seconds)", 
            total=None
        )
        # filter gspan warnings from console output
        warnings.simplefilter(action='ignore', category=FutureWarning)
        try:
            run_gspan_with_timeout(inputs)
        except timeout_decorator.timeout_decorator.TimeoutError:
            print("gSpan Miner execution finished.")
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"\n[bold green]Done![/bold green] See mining output in '{PATTERNS_FILE}'.")


def step2():
    ''' 
    - Convert patterns to graphs
    - Cluster
    - Generate plantUML *.txt files for patterns
    '''
    print(f"Loading patterns from '{PATTERNS_FILE}'...")
    pattern_graphs = utils.patterns.convertPatterns(PATTERNS_FILE)
    print("[bold green]Done![/bold green]\n")

    # clustering
    print("Clustering patterns...")
    patterns_features = utils.graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    patterns_dataframe = utils.graphClustering1.transform2singledataframe(patterns_features)
    patterns_similarity_matrix = utils.graphClustering1.calculate_similarity(patterns_dataframe)
    similarity_threshold = utils.command.ask_similarity_threshold()
    patterns_cluster_labels = utils.graphClustering1.group_similar_items(patterns_similarity_matrix, similarity_threshold)
    pattern_graphs_clustered = utils.graphClustering1.merge_lists(patterns_cluster_labels, pattern_graphs)
    print("[bold green]Done![/bold green]\n")
    
    if not os.path.exists(PATTERNS_DIR):
        os.mkdir(PATTERNS_DIR)

    print("Generating plantUML diagram text (*.txt) files...")
    for pattern in pattern_graphs_clustered:
        # file path: ./patterns/<cluster>/<pattern_support>_<pattern_index>.txt
        p_cluster_dir = os.path.join(PATTERNS_DIR, pattern[0]['pattern_cluster'])
        if not os.path.exists(p_cluster_dir):
            os.mkdir(p_cluster_dir)

        pattern_file = os.path.join(p_cluster_dir, f"{pattern[0]['pattern_support']}_{pattern[0]['pattern_index']}.txt")
        # bring pattern graph into standard graph structure 
        cleaned_pattern_graph = archimate.transform.clean_graph(pattern[1])
        archimate.visualization.generate_diagram(cleaned_pattern_graph[0], cleaned_pattern_graph[1], pattern_file)
    print(f"[bold green]Done![/bold green] See patterns output in '{PATTERNS_DIR}'\n")


def step2_diagrams(max_diagram_amount: int = None):
    '''
    Generate plantUML *.png files for patterns.
    Optionally set max amount of diagrams to generate through `max_diagram_amount`.
    '''
    generated_files = Path(PATTERNS_DIR).glob('**/*.txt')

    print("Generating plantUML diagram image (*.png) files...")
    for idx, txt_file in enumerate(generated_files, start=0):
        if max_diagram_amount != None and idx >= max_diagram_amount:
            break
        cmd = f"java -jar {PLANTUML_JAR_PATH} {txt_file}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Generated diagram for: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not generate diagram for {txt_file.name}: {e}")
    print(f"[bold green]Done![/bold green] See output in '{PATTERNS_DIR}'\n")


def step3():
    '''
    - Get domain information
    - Generate plantUML *.txt files for domain information
    '''
    # TODO: fully visualize truncated relationship element
    # TODO: add pattern support and index to diagrams
    pattern_graphs = utils.patterns.convertPatterns(PATTERNS_FILE)
    uploadgraphs = utils.patterns.load_graphs_from_pickle(PICKLE_FILE)
    archimate.filter.process_pattern(pattern_graphs, uploadgraphs, None)


def start():
    '''
    Full pipeline. Combines step1 - step3
    '''
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

    cleaned_pattern_graphs = []
    # create plantUML diagram text file for each pattern
    for pattern in pattern_graphs_clustered:
        # file path: ./patterns/<cluster>/<pattern_support>_<pattern_index>.txt
        p_cluster_dir = os.path.join(PATTERNS_DIR, pattern[0]['pattern_cluster'])
        if not os.path.exists(p_cluster_dir):
            os.mkdir(p_cluster_dir)
        pattern_file = os.path.join(p_cluster_dir, f"{pattern[0]['pattern_support']}_{pattern[0]['pattern_index']}.txt")
        
        # bring pattern graph into standard graph structure 
        cleaned_pattern_graph = archimate.transform.clean_graph(pattern[1])
        cleaned_pattern_graphs.append(cleaned_pattern_graph)
        archimate.visualization.generate_diagram(cleaned_pattern_graph[0], cleaned_pattern_graph[1], pattern_file)

    generated_files = Path(PATTERNS_DIR).glob('**/*.txt')

    '''
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
    '''
    utils.command.secondstop()
    
    # pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    uploadgraphs = utils.patterns.load_graphs_from_pickle('./input/graphs.pickle')

    '''
    generated_files2 = Path("./domain-patterns").glob('**/*.txt')
    for idx, txt_file in enumerate(generated_files2, start=0):
        cmd = f"java -jar {PLANTUML_JAR_PATH} {txt_file}"
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Generated diagram for: {txt_file}")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not generate diagram for {txt_file.name}: {e}")
    '''
    archimate.filter.process_pattern(pattern_graphs, uploadgraphs, None)