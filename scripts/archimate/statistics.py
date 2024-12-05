import archimate.pipeline
import archimate.types
from rich import print
import os

# Change this to the folder you want to generate statistics for
MODELS_DIR = './archimate/models_100_1000/'

def print_statistics():
    models = archimate.pipeline.import_models(MODELS_DIR)

    total_models = len(models)
    total_elements = 0
    total_relationships = 0
    total_business = 0
    total_application = 0
    total_technology = 0
    total_physical = 0
    total_motivation = 0
    total_strategy = 0
    total_implementation_migration = 0
    total_other = 0
    
    for m in models:
        elements = m['elements']
        relationships = m['relationships']
        total_elements += len(elements)
        total_relationships += len(relationships)

        for e in elements:
            if e['type'] in archimate.types.business_types:
                total_business += 1
            elif e['type'] in archimate.types.application_types:
                total_application += 1
            elif e['type'] in archimate.types.technology_types:
                total_technology +=1
            elif e['type'] in archimate.types.physical_types:
                total_physical += 1
            elif e['type'] in archimate.types.motivation_types:
                total_motivation += 1
            elif e['type'] in archimate.types.strategy_types:
                total_strategy += 1
            elif e['type'] in archimate.types.implementation_migration_types:
                total_implementation_migration += 1
            elif e['type'] in archimate.types.other_types:
                total_other += 1
    
    top_directory = os.path.basename(os.path.normpath(MODELS_DIR))
    print("\n--------------------------------------")
    print(f"Dataset: [green]{top_directory}[/]")
    print("--------------------------------------")
    print("[blue]General Info\n")
    print(f"Total models: {total_models}")    
    print(f"Total elements: {total_elements}")
    print(f"Total relationships: {total_relationships}")
    print("--------------------------------------")
    print("[blue]Elements per layer\n")
    print(f"Business: {total_business}")
    print(f"Application: {total_application}")
    print(f"Technology: {total_technology}")
    print(f"Physical: {total_physical}")
    print(f"Motivation: {total_motivation}")
    print(f"Strategy: {total_strategy}")
    print(f"Implementation & Migration: {total_implementation_migration}")
    print(f"Other: {total_other}")
    print("--------------------------------------")

        
