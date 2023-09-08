"""
This Python module represents a pipeline for performing graph pattern analysis using various utilities. 
It processes a collection of OntoUML models in JSON format, converts them into NetworkX graphs,
mines patterns using the gSpan algorithm, and generates PlantUML diagrams to visualize the patterns
"""


import os
import utils.ontoumlimport
import utils.generateinput
import utils.gspanMiner
import utils.patterns 
import utils.back2UML
import utils.graphClustering0
import utils.graphClustering1
import func_timeout
import utils.UMLviz
import utils.command
import signal
import subprocess
import os
import warnings
import networkx as nx

directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension
patternspath = "input/outputpatterns.txt" # replace with patterns file name
uml_folder = "./patterns"
plantuml_jar_path = "utils/plantumlGenerator.jar"
node_labels0 = ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                "creation", "historicalDependence", "manifestation", "participation",
                "participational", "termination", "triggers", "instantiation", "relation", "derivation"] 
edge_labels0 = ["target", "specific", "general","source", "generalization"]

file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)

#subkind pattern 0 - example
Gnodes = [('0', {'label': 'category'}),('1', {'label': 'functionalcomplex'}),('2', {'label': 'kind'}),('3', {'label': 'kind'}),('4', {'label': 'kind'})]
Gedges = [('0', '1', {'label': 'restrictedTo'}),('1', '2', {'label': 'restrictedTo'}),('1', '3', {'label': 'restrictedTo'}),('1', '4', {'label': 'restrictedTo'})]
G = nx.Graph()
G.add_nodes_from(Gnodes)
G.add_edges_from(Gedges)
subkind = [G]

if __name__ == "__main__":

    # Generate graphs from imported data
    graphs = utils.ontoumlimport.generateFullUndirected(file_names)
    
    # Filter class and relation labels
    class_labels = utils.command.filterClasses()
    relation_labels = utils.command.filterRelations()
    node_labels = class_labels + relation_labels
    edge_labels = utils.command.filterEdges()
    
    # Process graphs
    newgraphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
    newgraphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)
    
    # Save and process graphs
    downloadgraphs = utils.generateinput.save_graphs_to_pickle(newgraphs, './input/graphs.pickle')
    data = utils.generateinput.graphs_to_data_file(newgraphs_with_names, 'graphs')
    
    # Set parameters and run gSpan Miner
    gsParameters = utils.command.parameters()
    inputs = utils.gspanMiner.gsparameters(gsParameters)
    
    # Define timeout handler and run gSpan Miner
    try:
        patterns = func_timeout.func_timeout(10, utils.gspanMiner.run_gspan, args=(inputs,))
    except func_timeout.FunctionTimedOut:
        print("Function execution timed out")
    finally:
        utils.command.firststop()

    # Load and process pattern graphs
    uploadgraphs = utils.patterns.load_graphs_from_pickle('./input/graphs.pickle')
    known_patterns = utils.command.known_patterns()
    # pattern_graphs = utils.patterns.convertPatterns(patternspath)
    # pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    
    if known_patterns == "yes":
        pattern_graphs0 = utils.patterns.convertPatterns(patternspath)
        pattern_graphs = utils.patterns.remove_graphs_from_list(pattern_graphs0,subkind)
        pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    else:
        pattern_graphs = utils.patterns.convertPatterns(patternspath)
        pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    
    # Process pattern graphs for clustering
    patterns_features = utils.graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    patterns_dataframe = utils.graphClustering1.transform2singledataframe(patterns_features)
    patterns_similarity_matrix = utils.graphClustering1.calculate_similarity(patterns_dataframe)
    similarity_threshold = utils.command.ask_similarity_threshold()
    patterns_cluster_labels = utils.graphClustering1.group_similar_items(patterns_similarity_matrix,similarity_threshold)
    pattern_graphs_clustered_ = utils.graphClustering1.merge_lists(patterns_cluster_labels,pattern_graphs)
    pattern_graphs_clustered = utils.back2UML.process_genset_cardinalities(pattern_graphs_clustered_)
    
    # Convert pattern graphs to UML diagrams
    converted_patterns = utils.back2UML.convert_graphs_new(pattern_graphs_clustered)
    converted_patterns_filtered = utils.generateinput.process_graphs__(node_labels0, edge_labels0, converted_patterns)
    utils.UMLviz.convert_to_plantuml_clusters(converted_patterns_filtered)
    warnings.filterwarnings("ignore")

    # Generate PlantUML diagrams
    for root, dirs, files in os.walk(uml_folder):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            cmd = f"java -jar {plantuml_jar_path} {subfolder_path}"
            subprocess.run(cmd, shell=True, check=True)

    # Perform final processing and cleanup
    utils.command.secondstop()
    utils.command.process_pattern(pro_pattern_graphs, uploadgraphs, converted_patterns_filtered)
    utils.command.laststop()

