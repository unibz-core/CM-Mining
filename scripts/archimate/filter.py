from examples import custom_style_2
from PyInquirer import prompt, Separator
import archimate.types
from utils.command import NumberValidator

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
    