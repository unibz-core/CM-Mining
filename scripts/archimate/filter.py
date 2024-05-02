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

            # file path: ./domain-patterns/<pattern_index>_<pattern_support>
            dir_path = os.path.join(DOMAIN_PATTERNS_DIR, f"{pattern[0]['pattern_index']}_{pattern[0]['pattern_support']}/")
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            file_path = os.path.join(dir_path, f"{idx}.txt")
            title = f"{{ pattern_support: {pattern[0]['pattern_support']}, pattern_index: {pattern[0]['pattern_index']}, model_index: {pattern[0]['model_index']} }}"

            archimate.visualization.generate_diagram(
                cleaned_pattern_graph[0], 
                cleaned_pattern_graph[1], 
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
