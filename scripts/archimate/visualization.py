import os
from pathlib import Path
import networkx as nx
import archimate.types

def clean_str(s: str) -> str:
    s = ''.join(filter(str.isalnum, s))
    return s

def get_node_name(node: tuple) -> str:
    '''
    Transforms node to ArchiMate element in form of:
    ```
    Category_ElementName(ID, "Label")
    ```
    '''
    node_id, attributes = node
    node_label = attributes.get('label')

    category_mapping = {
        **dict.fromkeys(archimate.types.business_types, "Business"),
        **dict.fromkeys(archimate.types.application_types, "Application"),
        **dict.fromkeys(archimate.types.technology_types, "Technology"),
        **dict.fromkeys(archimate.types.physical_types, "Physical"),
        **dict.fromkeys(archimate.types.strategy_types, "Strategy"),
        **dict.fromkeys(archimate.types.implementation_migration_types, "Implementation"),
        **dict.fromkeys(archimate.types.motivation_types, "Motivation"),
        **dict.fromkeys(archimate.types.other_types, "Other")
    }

    # handle specific cases
    if node_label in ['Junction', 'AndJunction']:
        return f"Junction_And(\"{clean_str(node_id)}\", \"{node_label}\")\n"
    elif node_label == 'OrJunction':
        return f"Junction_Or(\"{clean_str(node_id)}\", \"{node_label}\")\n"
    elif node_label == 'Grouping':
        return f"Grouping(\"{clean_str(node_id)}\", \"{node_label}\")\n"

    category = category_mapping.get(node_label)
    if not category:
        print(f"[ERROR] Node label unknown: '{node_label}'")
        return ""

    # clear prefix if node label starts with category/layer, e.g., BusinessFunction -> Function
    if node_label.startswith(category):
        element_name = node_label.replace(category, '')
    else:
        element_name = node_label

    label0 = attributes.get('label0')
    if label0:
        if label0 == 'empty':
            label0 = ' '
        return f"{category}_{element_name}(\"{clean_str(node_id)}\", \"<size:10>//«{node_label}»//</size>\\n{label0}\")\n"
    else:
        return f"{category}_{element_name}(\"{clean_str(node_id)}\", \"{node_label}\")\n"


def get_relationship_text(edge: tuple) -> str:
    '''
    Transforms edge to ArchiMate relationship in form of:
    ```
    Rel_RelationType(source, target, "Label") 
    ```
    '''
    source, target, data = edge
    edge_label = data.get('label')

    if edge_label in archimate.types.relationship_types:
        return f"Rel_{edge_label}(\"{clean_str(source)}\", \"{clean_str(target)}\")\n"
    else:
        print(f"[ERROR] Edge label unknown: '{edge_label}'")
        return ""


def generate_diagram_text(graph: nx.Graph, truncated_edges: list, title: str = None) -> str: 
    plantuml_text = "@startuml\n!include <archimate/Archimate>\n\n"
    if title:
        plantuml_text += f"title {title}\n\n"

    # Category_ElementName(ID, Label)
    for node in graph.nodes(data=True):
        element_text = get_node_name(node)
        plantuml_text += element_text
    
    # Rel_RelationType(fromElement, toElement, "description")
    for edge in graph.edges(data=True):
        relationship_text = get_relationship_text(edge)
        plantuml_text += relationship_text

    special_source_types = ['source', 'specific']
    special_target_types = ['target', 'general']

    # handle truncated relationships
    for edge in truncated_edges:
        plantuml_text += f'rectangle "Element" as {clean_str(edge[0])} #line.dashed\n'

        if edge[2][0][2]['label'] in special_source_types:
            plantuml_text += f'Rel_{edge[1]}(\"{clean_str(edge[2][0][1])}\", \"{clean_str(edge[2][0][0])}\")\n'
        elif edge[2][0][2]['label'] in special_target_types:
            plantuml_text += f'Rel_{edge[1]}(\"{clean_str(edge[2][0][0])}\", \"{clean_str(edge[2][0][1])}\")\n'
        else:
            print(f"[ERROR] Unknown label in edge: {edge}")

    plantuml_text += "@enduml"
    return plantuml_text


def generate_diagram(graph: nx.Graph, truncated_edges: list, output_path: Path, title: str = None):
    '''
    Example diagram:
    ```
    @startuml
    !include <archimate/Archimate>
    
    Motivation_Stakeholder(1, "Stakeholder")
    Business_Service(2, "Business Service")

    Rel_Composition(1, 2, "Label")
    @enduml
    ```
    '''
    plantuml_text = generate_diagram_text(graph, truncated_edges, title)
    with open(output_path, 'w+') as f:
        f.write(plantuml_text)


def generate_diagrams(output_dir: str, graphs: list[nx.Graph]):
    '''
    Generates plantUML diagrams as .txt files out of the given list of networkX graphs
    and stores them in the given output directory.
    '''
    if not os.path.exists(output_dir):
        print(f"[ERROR] Could not generate diagrams, output directory '{output_dir}' does not exist.")
        return
    
    print("Generating plantUML diagrams...")
    for idx, graph in enumerate(graphs):
        filename = os.path.join(output_dir, f"graph_{idx}.txt")
        generate_diagram(graph, filename)
    print(f"Finished generating diagrams. See: {output_dir}")
