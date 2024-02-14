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
    'Product',
}
application_types = {
    'ApplicationComponent',
    'ApplicationCollaboration',
    'ApplicationInterface'
    'ApplicationProcess',
    'ApplicationFunction',
    'ApplicationInteraction',
    'ApplicationService',
    'ApplicationEvent',
    'DataObject',
}
technology_types = {
    'Facility',
    'Equipment'
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
    'DistributionNetwork',
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
    'Resource',
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
    # 'UsedBy', (equivalent to `Serving` relationship type, used in older ArchiMate models) -> needs to be normalized in dataset
}

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
