from examples import custom_style_2
from PyInquirer import prompt, Separator

'''
See ArchiMate Specification: 
https://pubs.opengroup.org/architecture/archimate32-doc/ch-Summary-of-Language-Notation.html
'''

business_types = {
    'BusinessActor',
    'BusinessRole',
    'BusinessCollaboration',
    'BusinessInterface',
    'BusinessProcess',
    'BusinessFunction',
    'BusinessInteraction',
    'BusinessService',
    'BusinessEvent',
    'BusinessObject',
    'Contract',
    'Representation',
    'Product'
}
application_types = {
    'ApplicationComponent',
    'ApplicationCollaboration',
    'ApplicationInterface',
    'ApplicationProcess',
    'ApplicationFunction',
    'ApplicationInteraction',
    'ApplicationService',
    'ApplicationEvent',
    'DataObject'
}
technology_types = {
    'Facility',
    'Equipment',
    'Material',
    'Node',
    'Device',
    'SystemSoftware',
    'TechnologyCollaboration',
    'TechnologyInterface',
    'TechnologyProcess',
    'TechnologyFunction',
    'TechnologyInteraction',
    'TechnologyService',
    'TechnologyEvent',
    'Artifact',
    'CommunicationNetwork',
    'Path',
    'DistributionNetwork'
}
motivation_types = {
    'Stakeholder',
    'Driver',
    'Assessment',
    'Goal',
    'Outcome',
    'Principle',
    'Requirement',
    'Constraint',
    'Value',
    'Meaning'
}
strategy_types = {
    'Resource', # structure element, but neither active nor passive
    'Capability',
    'ValueStream',
    'CourseOfAction'
}
implementation_migration_types = {
    'WorkPackage',
    'ImplementationEvent',
    'Deliverable',
    'Plateau',
    'Gap'
}
other_types = {
    'Location',
    'Grouping',
    'Junction',
    'OrJunction',
    'AndJunction'
}
relationship_types = {
    'Association',
    'Serving',
    'Flow',
    'Realization',
    'Aggregation',
    'Influence',
    'Composition',
    'Triggering',
    'Assignment',
    'Specialization',
    'Access'
}
layer_to_types = {
    "Business": business_types,
    "Application": application_types,
    "Technology": technology_types,
    "Motivation": motivation_types,
    "Strategy": strategy_types,
    "Implementation & Migration": implementation_migration_types,
    "Other": other_types
}
aspects = {
    'Active Structure': {
        'BusinessActor', 
        'BusinessRole', 
        'BusinessCollaboration',
        'BusinessInterface',
        'ApplicationComponent',
        'ApplicationCollaboration',
        'ApplicationInterface',
        'Node',
        'Device',
        'SystemSoftware',
        'TechnologyCollaboration',
        'TechnologyInterface',
        'CommunicationNetwork',
        'Path',
        'Facility',
        'Equipment',
        'DistributionNetwork',
    },
    'Behavior': {
        'BusinessProcess',
        'BusinessFunction',
        'BusinessInteraction',
        'BusinessService',
        'BusinessEvent',
        'ApplicationProcess',
        'ApplicationFunction',
        'ApplicationInteraction',
        'ApplicationService',
        'ApplicationEvent',
        'TechnologyProcess',
        'TechnologyFunction',
        'TechnologyInteraction',
        'TechnologyService',
        'TechnologyEvent',
        'Capability',
        'ValueStream',
        'CourseOfAction',
        'WorkPackage',
        'ImplementationEvent',
    },
    'Passive Structure': {
        'BusinessObject',
        'Contract',
        'Representation',
        'DataObject'
        'Artifact',
        'Material',
        'Deliverable',
        'Gap'
    },
    'Other': {
        'Product'  # composite
        'Plateau', # composite
        'Location',
        'Grouping',
        'Junction',
        'OrJunction',
        'AndJunction'
    },
    'Motivation': motivation_types
}

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
    layers = sorted(layer_to_types.keys())
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

    filtered_types = [t for choice in selected_choices for t in layer_to_types[choice]]
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
    filtered_types = [t for choice in selected_choices for t in aspects[choice]]
    print("Filtered element types:", filtered_types)
    return filtered_types


def filter_element_types():
    all_element_types = list(business_types.union(
        application_types, 
        technology_types, 
        motivation_types, 
        strategy_types, 
        implementation_migration_types, 
        other_types
    ))
    choices = [{'name': type_name} for type_name in sorted(all_element_types)]
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
    choices = [{'name': type_name} for type_name in sorted(list(relationship_types))]
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
