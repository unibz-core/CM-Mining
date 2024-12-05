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
}
physical_types = {
    'Equipment', 
    'DistributionNetwork', 
    'Facility', 
    'Material'
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
    "Physical": physical_types,
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