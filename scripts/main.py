import os
import utils.ontoumlimport
import utils.generateinput
import utils.gspanMiner
import utils.patterns 
import utils.back2UML
import utils.graphClustering0
import utils.graphClustering1
import utils.UMLviz
import utils.command
import signal
import subprocess
import os
import warnings


directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension
patternspath = "input/outputpatterns.txt" # replace with patterns file name
uml_folder = "./patterns"
plantuml_jar_path = "utils/plantumlGenerator.jar"
node_labels0 = ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                    "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                    "creation", "historicalDependence", "manifestation", "participation",
                    "participational", "termination", "triggers", "instantiation", "relation"] 
edge_labels0 = ["target", "specific", "general","source", "generalization"]

file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)

if __name__ == "__main__":

    graphs = utils.ontoumlimport.generateFullUndirected(file_names)
    class_labels = utils.command.filterClasses()
    relation_labels = utils.command.filterRelations()
    node_labels = class_labels + relation_labels
    edge_labels = utils.command.filterEdges()
    newgraphs = utils.generateinput.process_graphs(node_labels, edge_labels, graphs)
    newgraphs_with_names = utils.generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)
    #newgraphs = replace_labels_with_default(class_labels, relation_labels, edge_labels, graphs)
    downloadgraphs = utils.generateinput.save_graphs_to_pickle(newgraphs, './input/graphs.pickle')
    data = utils.generateinput.graphs_to_data_file(newgraphs_with_names, 'graphs')
    gsParameters = utils.command.parameters()
    print("Baking the output... ")
    inputs = utils.gspanMiner.gsparameters(gsParameters)
    
    def timeout_handler(signum, frame):
        raise TimeoutError("Function execution timed out")
    
    # Set the alarm signal to call the timeout_handler after 30 seconds
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(900)  # seconds
    try:
        patterns = utils.gspanMiner.run_gspan(inputs)
    except TimeoutError:
        print("Function execution timed out")
    finally:
        signal.alarm(0)
    utils.command.firststop()

    uploadgraphs = utils.patterns.load_graphs_from_pickle('./input/graphs.pickle')
    pattern_graphs = utils.patterns.convertPatterns(patternspath)
    pro_pattern_graphs = utils.patterns.return_all_domain_info(pattern_graphs)
    #patterns_features = utils.graphClustering.extract_features(pattern_graphs)
    patterns_features = utils.graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    #patterns_dataframe = utils.graphClustering.transform_graph_data(patterns_features)
    patterns_dataframe = utils.graphClustering1.transform2singledataframe(patterns_features)
    print("patterns_dataframe")
    print(patterns_dataframe)
    patterns_similarity_matrix = utils.graphClustering1.calculate_similarity(patterns_dataframe)
    print("patterns_similarity_matrix")
    print(patterns_similarity_matrix)
    similarity_threshold = utils.command.ask_similarity_threshold()
    patterns_cluster_labels = utils.graphClustering1.group_similar_items(patterns_similarity_matrix,similarity_threshold)
    pattern_graphs_clustered_ = utils.graphClustering1.merge_lists(patterns_cluster_labels,pattern_graphs)
    pattern_graphs_clustered = utils.back2UML.process_genset_cardinalities(pattern_graphs_clustered_)
    converted_patterns = utils.back2UML.convert_graphs_new(pattern_graphs_clustered)
    #patterns_cluster_viz = convert_to_plantuml_clusters(pattern_graphs_clustered)
   
    converted_patterns_filtered = utils.generateinput.process_graphs__(node_labels0, edge_labels0, converted_patterns)
    utils.UMLviz.convert_to_plantuml_clusters(converted_patterns_filtered)
    warnings.filterwarnings("ignore")

    # Iterate over subfolders in the uml folder
    for root, dirs, files in os.walk(uml_folder):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            cmd = f"java -jar {plantuml_jar_path} {subfolder_path}"
            subprocess.run(cmd, shell=True, check=True)

    utils.command.secondstop()
    utils.command.process_pattern(pro_pattern_graphs, uploadgraphs, converted_patterns_filtered)
    utils.command.laststop()



