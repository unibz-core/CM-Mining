import os
import networkx as nx
import test_patterns
import test_back2UML
import test_UMLviz
import test_graphClustering1
import test_generateinput
import warnings
import subprocess

def convert_to_plantuml_0(graphs, title="Caption"):
    os.makedirs("uml_patterns", exist_ok=True)
    file_paths = []
    for i, [index_dict,G] in enumerate(graphs):
        pattern_index = index_dict['pattern_index']
        lines = ["@startuml", f"title {index_dict}", "skin rose"]
        for node in G.nodes:
            label = G.nodes[node].get("label")#, str(node))
            label0 = G.nodes[node].get("label0")
            #label_with_id = f"{label}{node}"
            label_with_id = f"{label}{node}".replace(".", "")
            if label == "class":
                lines.append(f"class \"{label}_{label0}\" as {label_with_id}")
            elif label:
                lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")
        for edge in G.edges:
            source = G.nodes[edge[0]].get("label",str(edge[0]))
            source_with_id = f"{source}{edge[0]}".replace(".", "").replace("-", "")
            target = G.nodes[edge[1]].get("label",str(edge[1]))
            target_with_id = f"{target}{edge[1]}".replace(".", "").replace("-", "")
            label = G.edges[edge].get("label", "")
            label0 = G.edges[edge].get("label0", "")
            if label == "gen":
                lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
            elif label:
                lines.append(f"{source_with_id} <-- {target_with_id}: <<{label}>>: {label0}")
            else:
                lines.append(f"{source_with_id} <|-down- {target_with_id}")
        lines.append("@enduml")
        file_path = f"uml_patterns/{pattern_index}_uml.txt"
        with open(file_path, "w") as f:
            f.write("\n".join(lines))
        file_paths.append(file_path)
    return file_paths

import glob

def convert_to_plantuml_domain(graphs, title="Caption", output_folder="domain_patterns"):
    os.makedirs(output_folder, exist_ok=True)
    folder_paths = []
    pattern_counts = {}

    for i, [index_dict, G] in enumerate(graphs):
        lines = ["@startuml", f"title {index_dict}", "skin rose"]
        label_counts = {}  # Dictionary to keep track of label counts

        for node in G.nodes:
            label = G.nodes[node].get("label")
            label0 = G.nodes[node].get("label0")
            label_with_id = f"{label}{node}".replace(".", "")

            if label == "class":
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 0

                label0 = str(label_counts[label])  # Assign the index as label0
            
            # if label == "class":
            #     lines.append(f"class \"{label}_{label0}\" as {label_with_id}")
            # elif label:
            #     lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")
            if label == "class":
                lines.append(f"class \"{label}_{label0}\" as {label_with_id}")
            elif label in ["collective", "functionalcomplex", "quantity", "intrinsicmode", "extrinsicmode",
                           "quality", "relator", "abstract", "event", "situation", "type"] :
                lines.append(f"class \"{label}\" as {label_with_id} #line.dotted:blue")
            elif label:
                lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

            #lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

        for edge in G.edges:
            source = G.nodes[edge[0]].get("label", str(edge[0]))
            source_with_id = f"{source}{edge[0]}".replace(".", "")
            target = G.nodes[edge[1]].get("label", str(edge[1]))
            target_with_id = f"{target}{edge[1]}".replace(".", "")
            label = G.edges[edge].get("label", "")
            label0 = G.edges[edge].get("label0", "")

            # if label == "gen":
            #     lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
            # elif label == "relation":
            #     lines.append(f"{source_with_id} <-- {target_with_id}: {label}: {label0}")
            # elif label:
            #     lines.append(f"{source_with_id} <-- {target_with_id}: <<{label}>>: {label0}")
            # else:
            #     lines.append(f"{source_with_id} <|-down- {target_with_id}")
            if label == "gen":
                lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
            elif label == "relation":
                lines.append(f"{source_with_id} <-- {target_with_id}: {label}: {label0}")
            elif label == "restrictedto":
                lines.append(f"{source_with_id} .[#blue,dotted,thickness=2]. {target_with_id}: {label}: {label0}")
            elif label:
                lines.append(f"{source_with_id} <-- {target_with_id}: <<{label}>>: {label0}")
            else:
                lines.append(f"{source_with_id} <|-down- {target_with_id}")

        lines.append("hide circle")
        lines.append("hide members")
        lines.append("@enduml")
        pattern_index = index_dict['pattern_index']
        pattern_support = index_dict['pattern_support']
        folder_path = os.path.join(output_folder, f"{pattern_index}_{pattern_support}")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{i}_uml.txt")

        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        folder_paths.append(folder_path)
        pattern_counts[pattern_index] = pattern_counts.get(pattern_index, 0) + 1

        print(f"Generated: {file_path}")  # Print file path after generation

    for pattern_index, count in pattern_counts.items():
        subfolder = os.path.join(output_folder, f"{pattern_index}_*")
        matching_folders = glob.glob(subfolder)
        for folder in matching_folders:
            folder_name = os.path.basename(folder)
            new_folder_name = f"{folder_name}_{count}"
            new_folder_path = os.path.join(output_folder, new_folder_name)
            os.rename(folder, new_folder_path)

    return folder_paths

def convert_to_plantuml_clusters(graphs, title="Caption", output_folder="patterns"):
    os.makedirs(output_folder, exist_ok=True)
    folder_paths = []
    pattern_counts = {}

    for i, [index_dict, G] in enumerate(graphs):
        lines = ["@startuml", f"title {index_dict}", "skin rose"]
        label_counts = {}  # Dictionary to keep track of label counts

        for node in G.nodes:
            label = G.nodes[node].get("label")
            label0 = G.nodes[node].get("label0")
            label_with_id = f"{label}{node}".replace(".", "")

            if label == "class":
                if label in label_counts:
                    label_counts[label] += 1
                else:
                    label_counts[label] = 0

                label0 = str(label_counts[label])  # Assign the index as label0
            
            if label == "class":
                lines.append(f"class \"{label}_{label0}\" as {label_with_id}")
            elif label in ["collective", "functionalcomplex", "quantity", "intrinsicmode", "extrinsicmode",
                           "quality", "relator", "abstract", "event", "situation", "type"] :
                lines.append(f"class \"{label}\" as {label_with_id} #line.dotted:blue")
            elif label:
                lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

            #lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

        for edge in G.edges:
            source = G.nodes[edge[0]].get("label", str(edge[0]))
            source_with_id = f"{source}{edge[0]}".replace(".", "")
            target = G.nodes[edge[1]].get("label", str(edge[1]))
            target_with_id = f"{target}{edge[1]}".replace(".", "")
            label = G.edges[edge].get("label", "")
            label0 = G.edges[edge].get("label0", "")

            if label == "gen":
                lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
            elif label == "relation":
                lines.append(f"{source_with_id} <-- {target_with_id}: {label}: {label0}")
            elif label == "restrictedto":
                lines.append(f"{source_with_id} .[#blue,dotted,thickness=2]. {target_with_id}: {label}: {label0}")
            elif label:
                lines.append(f"{source_with_id} <-- {target_with_id}: <<{label}>>: {label0}")
            else:
                lines.append(f"{source_with_id} <|-down- {target_with_id}")
        lines.append("hide circle")
        lines.append("hide members")
        lines.append("@enduml")
        pattern_index = index_dict['pattern_index']
        pattern_support = index_dict['pattern_support']
        pattern_cluster = index_dict['pattern_cluster']
        folder_path = os.path.join(output_folder, f"{pattern_cluster}")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{pattern_index}_{pattern_support}_uml.txt")

        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        folder_paths.append(folder_path)
        pattern_counts[pattern_index] = pattern_counts.get(pattern_index, 0) + 1

        print(f"Generated: {file_path}")  # Print file path after generation

    return folder_paths

#oldVIZ

#this is great!!!!!!!!
#https://stackoverflow.com/questions/39657395/how-to-draw-properly-networkx-graphs

import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for plotting without a display

def visualize_graphs(graphs, subtitles):
    assert len(graphs) == len(subtitles), "Number of graphs and subtitles must be the same"

    pattern_indices = list(set([subtitle['pattern_index'] for subtitle in subtitles]))

    for pattern_index in pattern_indices:
        folder_name = f'domaindots/{pattern_index}'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_count = 0
        model_index_set = set()
        for model_index, subtitle in enumerate(subtitles):
            if subtitle['pattern_index'] != pattern_index:
                continue

            fig, ax = plt.subplots(figsize=(9, 8))
            pos = nx.nx_pydot.graphviz_layout(graphs[model_index], prog='dot')
            pos = {k: (-v[0], -v[1]) for k, v in pos.items()}
            nx.draw(graphs[model_index], pos, with_labels=False, font_size=10, font_weight='bold', node_color='b', alpha=0.2)
            nlabels = {k: f"{d.get('label', '')} {d.get('label0', '')}" for k, d in graphs[model_index].nodes(data=True)}
            elabels = nx.get_edge_attributes(graphs[model_index], 'label')
            nx.draw_networkx_edge_labels(graphs[model_index], pos, edge_labels=elabels, font_size=7, font_weight='bold')
            nx.draw_networkx_labels(graphs[model_index], pos, labels=nlabels, font_size=7, font_weight='bold')
            ax.set_title(subtitle, fontsize=7, loc='center', wrap=True, pad=12, color='black',
                         bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.9'))
            fig.subplots_adjust(left=0.03, right=0.95, bottom=0.05, top=0.83, wspace=1.00, hspace=0.3)
            plt.savefig(f'{folder_name}/graph_{model_index}.png', dpi=300, bbox_inches=None)
            plt.close()

            file_count += 1
            model_index_set.add(subtitle['model_index'])

        label = f"{file_count}_{len(model_index_set)}"
        os.rename(folder_name, f"{folder_name}_{label}")

    plt.close('all')  # Close all open figures

import os
import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph_patterns(graphs):
    for i, [index,graph] in enumerate(graphs):
        folder_name = 'domaindots'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        fig, ax = plt.subplots(figsize=(7, 7))
        pos = nx.nx_pydot.graphviz_layout(graph, prog='dot') 
        pos = {k: (-v[0], -v[1]) for k, v in pos.items()}
        nx.draw(graph, pos, with_labels=False, font_size=10, font_weight='bold', node_color='b', alpha=0.2)
        nlabels = nx.get_node_attributes(graph, 'label')
        elabels = nx.get_edge_attributes(graph, 'label')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=elabels, font_size=7, font_weight='bold')
        nx.draw_networkx_labels(graph, pos, labels=nlabels, font_size=7, font_weight='bold')
        ax.set_title(f"Pattern {index}", fontsize=7, loc='center', wrap=True, pad=12, color='black', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.4'))
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.83, wspace=0.6, hspace=0.3)
        plt.savefig(f'{folder_name}/{index}_pattern.png', dpi=300, bbox_inches=None)
        plt.close()

    #plt.show()
    plt.close('all')

node_labels0 = ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                    "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                    "creation", "historicalDependence", "manifestation", "participation",
                    "participational", "termination", "triggers", "instantiation", "relation"] 
edge_labels0 = ["target", "specific", "general","source", "generalization"]

patternspath = "input_/outputpatterns.txt" 
uml_folder = "./patterns"
plantuml_jar_path = "plantumlGenerator.jar"

pattern_graphs = test_patterns.convertPatterns(patternspath)

pattern_graphs = test_patterns.convertPatterns(patternspath)
pro_pattern_graphs = test_patterns.return_all_domain_info(pattern_graphs)
#patterns_features = utils.graphClustering.extract_features(pattern_graphs)
patterns_features = test_graphClustering1.graphs2dataframes2vectors(pattern_graphs)
#patterns_dataframe = utils.graphClustering.transform_graph_data(patterns_features)
patterns_dataframe = test_graphClustering1.transform2singledataframe(patterns_features)
print("patterns_dataframe")
print(patterns_dataframe)
patterns_similarity_matrix = test_graphClustering1.calculate_similarity(patterns_dataframe)
print("patterns_similarity_matrix")
print(patterns_similarity_matrix)
patterns_cluster_labels = test_graphClustering1.group_similar_items(patterns_similarity_matrix,0.4)
pattern_graphs_clustered_ = test_graphClustering1.merge_lists(patterns_cluster_labels,pattern_graphs)
pattern_graphs_clustered = test_back2UML.process_genset_cardinalities(pattern_graphs_clustered_)
converted_patterns = test_back2UML.convert_graphs_new(pattern_graphs_clustered)
#patterns_cluster_viz = convert_to_plantuml_clusters(pattern_graphs_clustered)

converted_patterns_filtered = test_generateinput.process_graphs__(node_labels0, edge_labels0, converted_patterns)
test_UMLviz.convert_to_plantuml_clusters(converted_patterns_filtered)

warnings.filterwarnings("ignore")

 # Iterate over subfolders in the uml folder
for root, dirs, files in os.walk(uml_folder):
    for dir in dirs:
        subfolder_path = os.path.join(root, dir)
        cmd = f"java -jar {plantuml_jar_path} {subfolder_path}"
        subprocess.run(cmd, shell=True, check=True)

