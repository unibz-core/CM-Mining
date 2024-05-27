import os
import subprocess
from examples import custom_style_2
from PyInquirer import prompt, Separator
import archimate.pipeline
import archimate.types
from utils.command import NumberValidator
from rich import print
import utils.patterns

def select_element_filter_kind():
    choices = ["Layers", "Aspects", "Specific Types"]
    question = [
        {
            'type': 'list',
            'message': 'Filter elements by:',
            'name': 'selected_kind',
            'choices': [
                {
                    'name': string
                }
                for string in choices
            ]     
        }
    ]
    answer = prompt(question, style=custom_style_2)
    selected_choice = answer['selected_kind']
    print("Selected element filter kind:", selected_choice)
    return selected_choice


def filter_layers():
    layers = sorted(archimate.types.layer_to_types.keys())
    choices = [{'name': layer} for layer in layers]
    question = [
        {
            'type': 'checkbox',
            'message': 'Select element types to filter out:',
            'name': 'selected_layers',
            'choices': choices
        }
    ]
    answers = prompt(question, style=custom_style_2)
    selected_choices = answers['selected_layers']
    print("Selected layers to filter:", selected_choices)

    filtered_types = [t for choice in selected_choices for t in archimate.types.layer_to_types[choice]]
    print("Filtered element types:", filtered_types)
    return filtered_types


def filter_aspects():
    strings = ["Active Structure", "Passive Structure", "Behavior", "Other", "Motivation"]
    question = [
        {
            'type': 'checkbox',
            'message': 'Select edges to filter-out:',
            'name': 'selected_strings',
            'choices': [
                {
                    'name': string
                }
                for string in strings
            ]
        }
    ]
    answers = prompt(question, style=custom_style_2)
    selected_choices = answers['selected_strings']
    print("Selected aspect filters:", selected_choices)
    filtered_types = [t for choice in selected_choices for t in archimate.types.aspects[choice]]
    print("Filtered element types:", filtered_types)
    return filtered_types


def filter_element_types():
    all_element_types = sorted(list(archimate.types.business_types.union(
        archimate.types.application_types, 
        archimate.types.technology_types, 
        archimate.types.physical_types,
        archimate.types.motivation_types, 
        archimate.types.strategy_types, 
        archimate.types.implementation_migration_types, 
        archimate.types.other_types
    )))
    choices = [{'name': type_name} for type_name in all_element_types]
    question = [
        {
            'type': 'checkbox',
            'message': 'Select element types to filter out:',
            'name': 'selected_types',
            'choices': choices
        }
    ]
    answers = prompt(question, style=custom_style_2)
    selected_choices = answers['selected_types']
    print(selected_choices)
    print("Selected element type filters:", selected_choices)
    return selected_choices


def filter_relationship_types():
    rel_types = sorted(list(archimate.types.relationship_types))
    choices = [{'name': type_name} for type_name in rel_types]
    question = [
        {
            'type': 'checkbox',
            'message': 'Select relationship types to filter out:',
            'name': 'selected_types',
            'choices': choices
        }
    ]
    answers = prompt(question, style=custom_style_2)
    selected_choices = answers['selected_types']
    print("Selected relationship type filters:", selected_choices)
    return selected_choices


def filter_edge_labels():
    strings = ["source", "target", "specific", "general"]
    question = [
        {
            'type': 'checkbox',
            'message': 'Select edges to filter-out:',
            'name': 'selected_strings',
            'choices': [
                {
                    'name': string
                }
                for string in strings
            ]
        }
    ]
    answers = prompt(question, style=custom_style_2)
    selected_choices = answers['selected_strings']
    print("Selected edge label filters:", selected_choices)
    return selected_choices

def input_max_diagram_amount():
    question = [
        {
            'type': "input",
            "name": "max_amount",
            "message": "Enter the maximum amount of diagrams to generate as an image (*.png) file",
            "validate": NumberValidator,
            "filter": lambda val: int(val)
        }
    ]
    answer = prompt(question, style=custom_style_2)
    max_amount = answer['max_amount']
    print(f"Maximum amount of diagram to generate as images: {max_amount}")
    return max_amount


def fix_graphs(pattern_graph, host_graph):
    host_edges = {(u, v, d['label']) for u, v, d in host_graph.edges(data=True)}
    edges_to_reverse = []

    for u, v, d in pattern_graph.edges(data=True):
        edge_label = d['label']
        if (u, v, edge_label) not in host_edges and (v, u, edge_label) in host_edges:
            # if the edge is inverted, add to the list of edges to reverse
            edges_to_reverse.append((u, v))

    # reverse the edges in the pattern_graph
    for u, v in edges_to_reverse:
        edge_data = pattern_graph[u][v]
        pattern_graph.remove_edge(u, v)
        pattern_graph.add_edge(v, u, **edge_data)

    return pattern_graph


def process_pattern(pattern_graphs, host_graphs, converted_patterns_filtered):
    stored_integers = set()
    DOMAIN_PATTERNS_DIR = './domain-patterns/'
    
    while True:
        questions = [
            {
                'type': 'input',
                'name': 'patterns',
                'message': 'Enter a pattern index:',
                'validate': lambda val: val.isdigit() or 'Please enter a valid pattern'
            }
        ]
        answers = prompt(questions)
        integer = int(answers['patterns'])
        if integer in stored_integers:
            print("This patterns has already been entered. Please enter a different pattern.")
            continue
        stored_integers.add(integer)
        print(f"Selected pattern_index: {integer}")

        selected_pattern = utils.patterns.select_sublists(pattern_graphs, [str(integer)])
        find_patterns = utils.patterns.count_subgraph_isomorphisms(selected_pattern, host_graphs)
        find_patterns_cleaned = utils.patterns.remove_duplicate_graphs(find_patterns)

        generated_files = []
        if not os.path.exists(DOMAIN_PATTERNS_DIR):
            os.mkdir(DOMAIN_PATTERNS_DIR)

        for idx, pattern in enumerate(find_patterns_cleaned, start=0):
            cleaned_pattern_graph = archimate.transform.clean_graph(pattern[1])

            host_graph = host_graphs[pattern[0]['model_index']]
            host_edges = list(host_graph.edges(data=True))
            host_nodes = list(host_graph.nodes(data=True))
            truncated_edges = cleaned_pattern_graph[1]

            for edge in truncated_edges:
                edge_id = edge[0]
                found_edges = [e for e in host_edges if e[0] == edge_id or e[1] == edge_id]
                # sometimes source or target node is missing (e.g., when element is part of a filtered layer)
                if len(found_edges) != 2:
                    print(f"WARNING: Could not visualize truncated edge: {edge}")
                    continue

                source_node = found_edges[0][0]
                target_node = found_edges[1][0]

                existing_node = source_node if source_node in cleaned_pattern_graph[0] else target_node
                node_to_add = target_node if existing_node == source_node else source_node
                node_data = next(node[1] for node in host_nodes if node[0] == node_to_add)
                cleaned_pattern_graph[0].add_node(node_to_add, **node_data)

                if (node_to_add, edge_id, {'label': 'source'}) in host_edges:
                    cleaned_pattern_graph[0].add_edge(node_to_add, existing_node, label=edge[1])
                elif (node_to_add, edge_id, {'label': 'specific'}) in host_edges:
                    cleaned_pattern_graph[0].add_edge(node_to_add, existing_node, label=edge[1])
                elif (existing_node, edge_id, {'label': 'source'}) in host_edges:
                    cleaned_pattern_graph[0].add_edge(existing_node, node_to_add, label=edge[1])
                elif (existing_node, edge_id, {'label': 'specific'}) in host_edges:
                    cleaned_pattern_graph[0].add_edge(existing_node, node_to_add, label=edge[1])
                else:
                    print("WARNING")

            # file path: ./domain-patterns/<pattern_index>_<pattern_support>
            dir_path = os.path.join(DOMAIN_PATTERNS_DIR, f"{pattern[0]['pattern_index']}_{pattern[0]['pattern_support']}/")
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            file_path = os.path.join(dir_path, f"{idx}.txt")
            title = f"{{ pattern_support: {pattern[0]['pattern_support']}, pattern_index: {pattern[0]['pattern_index']}, model_index: {pattern[0]['model_index']} }}"

            fixed_pattern_graph = fix_graphs(cleaned_pattern_graph[0], host_graph)
            archimate.visualization.generate_diagram(
                fixed_pattern_graph, 
                [],
                file_path,
                title
            )
            generated_files.append(file_path)

        print("Generating plantUML diagrams...")
        
        for idx, txt_file in enumerate(generated_files, start=0):
            cmd = f"java -jar {archimate.pipeline.PLANTUML_JAR_PATH} {txt_file}"
            try:
                subprocess.run(cmd, shell=True, check=True)
                print(f"Generated diagram for: {txt_file}")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Could not generate diagram for {txt_file.name}: {e}")
        
        print(f"[bold green]Done![/bold green]\n")

        # Ask if user wants to continue
        questions = [
            {
                'type': 'confirm',
                'name': 'continue',
                'message': 'Do you want to continue?',
                'default': False
            }
        ]
        answers = prompt(questions)
        if not answers['continue']:
            break

    utils.command.laststop()      
