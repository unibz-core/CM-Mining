"""
This Python module provides functions for converting a list of 
NetworkX graphs into PlantUML diagrams for different purposes
"""

import os
import networkx as nx
import glob

def convert_to_plantuml_domain(graphs, title="Caption", output_folder="domain_patterns"):
    """
    Convert a list of network graphs into PlantUML diagrams for individual domains.

    :param graphs: List of graph-pattern pairs.
    :param title: Title of the PlantUML diagram. (default: "Caption")
    :param output_folder: Output folder path for saving the diagrams. (default: "domain_patterns")
    :return: List of folder paths where the diagrams are saved.
    """
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
                #lines.append(f"class \"{label}_{label0}\" as {label_with_id}")
                lines.append(f"class \"{label}_{label0}\" as {label_with_id} #line.dotted:blue" )
            elif label in ["_collective_", "_functionalcomplex_", "_quantity_", "_intrinsicmode_", "_extrinsicmode_",
                "_quality_", "_relator_", "_abstract_", "_event_", "_situation_", "_type_"]:
                lines.append(f"class \"{label}\" as {label_with_id} #line.dotted:blue")
            elif label:
                lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

        for edge in G.edges:
            source = G.nodes[edge[0]].get("label", str(edge[0]))
            source_with_id = f"{source}{edge[0]}".replace(".", "")
            target = G.nodes[edge[1]].get("label", str(edge[1]))
            target_with_id = f"{target}{edge[1]}".replace(".", "")
            label = G.edges[edge].get("label", "")
            label0 = G.edges[edge].get("label0", "")

            if label == "gen":
                #lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
                lines.append(f"{target_with_id} <|-down- {source_with_id}: Generalization {label0}")
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


def extract_strings(input_string):
    """
    Used to split cardinalities and show them correctly in the final plantuml diagram.
    """

    if not input_string:
        #return '".."', '".."'
        return '', ''
    
    left, right = input_string.split('_')
    
    if '*' in left:
        left = '"' + left.replace('*', '') + '*"'
    else:
        left = '"' + left + '"'
    
    right = '"' + right + '"'
    
    return left, right

def convert_to_plantuml_clusters(graphs, title="Caption", output_folder="patterns"):
    """
    Convert a list of network graphs into PlantUML diagrams for patterns within clusters.

    :param graphs: List of graph-pattern pairs.
    :param title: Title of the PlantUML diagram. (default: "Caption")
    :param output_folder: Output folder path for saving the diagrams. (default: "patterns")
    :return: List of folder paths where the diagrams are saved.
    """
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
                #lines.append(f"class \"{label}_{label0}\" as {label_with_id}" )
                lines.append(f"class \"{label}_{label0}\" as {label_with_id} #line.dotted:blue" )
            elif label in ["_collective_", "_functionalcomplex_", "_quantity_", "_intrinsicmode_", "_extrinsicmode_",
                           "_quality_", "_relator_", "_abstract_", "_event_", "_situation_", "_type_"] :
                lines.append(f"class \"{label}\" as {label_with_id} #line.dotted:blue")
            elif label:
                lines.append(f"class \"{label0}\" as {label_with_id} <<{label}>>")

        for edge in G.edges:
            source = G.nodes[edge[0]].get("label", str(edge[0]))
            source_with_id = f"{source}{edge[0]}".replace(".", "")
            target = G.nodes[edge[1]].get("label", str(edge[1]))
            target_with_id = f"{target}{edge[1]}".replace(".", "")
            label = G.edges[edge].get("label", "")
            label0 = G.edges[edge].get("label0", "")
            left_str, right_str = extract_strings(label0)

            if label == "gen":
                #lines.append(f"{target_with_id} <|-down- {source_with_id}: {label} {label0}")
                lines.append(f"{target_with_id} <|-down- {source_with_id}: Generalization {label0}")
            elif label == "relation":
                #lines.append(f"{source_with_id} <-- {target_with_id}: {label}: {label0}")
                lines.append(f"{source_with_id} {right_str} <-- {left_str} {target_with_id}: {label}")
            elif label == "restrictedto":
                lines.append(f"{source_with_id} .[#blue,dotted,thickness=2]. {target_with_id}: {label}: {label0}")
            elif label:
                #lines.append(f"{source_with_id} <-- {target_with_id}: <<{label}>>: {label0}")
                lines.append(f"{source_with_id} {right_str} <-- {left_str} {target_with_id}: <<{label}>>: ")
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
        #file_path = os.path.join(folder_path, f"{pattern_index}_{pattern_support}_uml.txt")
        file_path = os.path.join(folder_path, f"{pattern_support}_{pattern_index}_uml.txt")

        with open(file_path, "w") as f:
            f.write("\n".join(lines))

        folder_paths.append(folder_path)
        pattern_counts[pattern_index] = pattern_counts.get(pattern_index, 0) + 1

        print(f"Generated: {file_path}")  # Print file path after generation

    return folder_paths



