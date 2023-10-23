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
import func_timeout
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

#subkind pattern "A"
sAnodes = [('0', {'label': 'kind'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'subkind'}),('4', {'label': 'subkind'})]
sAedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('1', '3', {'label': 'specific'}),('2', '4', {'label': 'specific'})]
sA = nx.Graph()
sA.add_nodes_from(sAnodes)
sA.add_edges_from(sAedges)

#subkind pattern "B"
sBnodes = [('0', {'label': 'kind'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'gen'}),('4', {'label': 'subkind'}),('5', {'label': 'subkind'}),('6', {'label': 'subkind'})]
sBedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('0', '3', {'label': 'general'}),('1', '4', {'label': 'specific'}),('2', '5', {'label': 'specific'}),('3', '6', {'label': 'specific'})]
sB = nx.Graph()
sB.add_nodes_from(sBnodes)
sB.add_edges_from(sBedges)

#category pattern "A"
cAnodes = [('0', {'label': 'category'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'kind'}),('4', {'label': 'kind'})]
cAedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('1', '3', {'label': 'specific'}),('2', '4', {'label': 'specific'})]
cA = nx.Graph()
cA.add_nodes_from(cAnodes)
cA.add_edges_from(cAedges)

#category pattern "B"
cBnodes = [('0', {'label': 'category'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'gen'}),('4', {'label': 'subkind'}),('5', {'label': 'subkind'}),('6', {'label': 'subkind'})]
cBedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('0', '3', {'label': 'general'}),('1', '4', {'label': 'specific'}),('2', '5', {'label': 'specific'}),('3', '6', {'label': 'specific'})]
cB = nx.Graph()
cB.add_nodes_from(cBnodes)
cB.add_edges_from(cBedges)

#phase pattern "A"
pAnodes = [('0', {'label': 'kind'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'phase'}),('4', {'label': 'phase'})]
pAedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('1', '3', {'label': 'specific'}),('2', '4', {'label': 'specific'})]
pA = nx.Graph()
pA.add_nodes_from(pAnodes)
pA.add_edges_from(pAedges)

#phase pattern "B"
pBnodes = [('0', {'label': 'kind'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'gen'}),('4', {'label': 'phase'}),('5', {'label': 'phase'}),('6', {'label': 'phase'})]
pBedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('0', '3', {'label': 'general'}),('1', '4', {'label': 'specific'}),('2', '5', {'label': 'specific'}),('3', '6', {'label': 'specific'})]
pB = nx.Graph()
pB.add_nodes_from(pBnodes)
pB.add_edges_from(pBedges)

#relator pattern "A"
rAnodes = [('0', {'label': 'relator'}),('1', {'label': 'role'}),('2', {'label': 'role'}),('3', {'label': 'mediation'}),('4', {'label': 'mediation'})]
rAedges = [('0', '3', {'label': 'source'}),('3', '1', {'label': 'target'}),('0', '4', {'label': 'source'}),('4', '2', {'label': 'target'})]
rA = nx.Graph()
rA.add_nodes_from(rAnodes)
rA.add_edges_from(rAedges)

#roleMixin pattern "A"
rmAnodes = [('0', {'label': 'rolemixin'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),('3', {'label': 'role'}),('4', {'label': 'role'})]
rmAedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),('1', '3', {'label': 'specific'}),('2', '4', {'label': 'specific'})]
rmA = nx.Graph()
rmA.add_nodes_from(rmAnodes)
rmA.add_edges_from(rmAedges)

#roleMixin pattern "B"
rmBnodes = [('0', {'label': 'rolemixin'}),('1', {'label': 'gen'}),('2', {'label': 'gen'}),
            ('3', {'label': 'role'}),('4', {'label': 'role'}),('5', {'label': 'gen'}),
            ('6', {'label': 'gen'}),('7', {'label': 'kind'}),('8', {'label': 'kind'})]
rmBedges = [('0', '1', {'label': 'general'}),('0', '2', {'label': 'general'}),
            ('1', '3', {'label': 'specific'}),('2', '4', {'label': 'specific'}),('7', '5', {'label': 'general'}),('5', '3', {'label': 'specific'}),('8', '6', {'label': 'general'}),('6', '4', {'label': 'specific'})]
rmB = nx.Graph()
rmB.add_nodes_from(rmAnodes)
rmB.add_edges_from(rmAedges)


kpattenrs = [sA,sB,cA,cB,pA,pB,rA,rmA,rmB]

if __name__ == "__main__":

    # Generate graphs from imported data
    print("Importing models...")
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
    patterns = ""
    try:
        patterns = func_timeout.func_timeout(900, utils.gspanMiner.run_gspan, args=(inputs,))
    except func_timeout.FunctionTimedOut:
        print("Function execution timed out")
    if patterns is not None:
        utils.command.firststop()

    # Load and process pattern graphs
    uploadgraphs = utils.patterns.load_graphs_from_pickle('./input/graphs.pickle')
    known_patterns = utils.command.known_patterns()
    
    if known_patterns == "yes":
        pattern_graphs0 = utils.patterns.convertPatterns(patternspath)
        pattern_graphs = utils.patterns.remove_graphs_from_list(pattern_graphs0,kpattenrs)
        pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    else:
        pattern_graphs = utils.patterns.convertPatterns(patternspath)
        pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs) 
    #print(pattern_graphs0)
    #print(pattern_graphs)

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

