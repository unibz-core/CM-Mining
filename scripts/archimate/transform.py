import os, pickle
import networkx as nx
from pathlib import Path
import archimate.types


def clean_graphs(graphs: list[nx.Graph]) -> list[nx.Graph]:
    rel_types = archimate.types.relationship_types
    special_source_types = ['source', ] # add general/specific
    special_target_types = ['target', ] # add general/specific
    cleaned_graphs = []

    for graph in graphs:
        new_graph = nx.Graph()
        intermediate_edges = []
        # id: 1 
        # type: Composition
        # source 

        for node, data in graph.nodes(data=True):
            if data['label'] not in rel_types:
                new_graph.add_node(node, **data)

        for node, data in graph.nodes(data=True):
            if data['label'] in rel_types:
                source_target_edges = graph.edges(node, data=True)
                if len(source_target_edges) != 2:
                    continue
                
                source = None
                target = None
                for u, v, data2 in source_target_edges:
                    if data2['relation'] in special_source_types:
                        source = v
                    if data2['relation'] in special_target_types:
                        target = v
                
                if source is None or target is None:
                    continue
                
                new_graph.add_edge(source, target, **data)

        cleaned_graphs.append(new_graph)
    
    return cleaned_graphs


def convert_to_graph(patterns_file: Path) -> list[nx.Graph]:
    graphs = []
    current_graph = None

    with open(patterns_file, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split(' ')
            
            # start of a new graph
            if parts[0] == 't':  
                if current_graph is not None:
                    graphs.append(current_graph)
                current_graph = nx.Graph()
            elif parts[0] == 'v' and current_graph is not None:
                current_graph.add_node(int(parts[1]), label=parts[2])
            elif parts[0] == 'e' and current_graph is not None:
                current_graph.add_edge(int(parts[1]), int(parts[2]), relation=parts[3])
    # add last processed graph
    if current_graph not in graphs:
        graphs.append(current_graph)

    return graphs

def create_graphs(models: list[dict], output_dir: Path) -> list[list]:
    graphs = []
    file_names = []
    gspan_output_file = os.path.join(output_dir, 'graphs.data')
    with open(gspan_output_file, 'w'):
        # create empty file
        pass
    
    for i, m in enumerate(models):
        # create a new subgraph for each model
        SG = nx.Graph()
        with open(gspan_output_file, 'a') as outfile:
            outfile.write(f"t # {i} {m['archimateId']}\n")
            
            id_to_idx = {}
            count = 0

            # map elements to nodes
            for idx, e in enumerate(m['elements'], 1):
                id_to_idx[e['id']] = idx
                label0 = e['name'] if e['name'] != '' else 'empty'
                SG.add_node(e['id'], label=e['type'], label0=label0)
                outfile.write(f"v {idx} {e['type']}\n")
                count = idx

            # map relationships to nodes and connect with source/target
            for idx, r in enumerate(m['relationships'], count):
                id_to_idx[r['id']] = idx
                SG.add_node(r['id'], label=r['type'])
                
                if r['type'] == 'Specialization':
                    SG.add_edge(r['id'], r['sourceId'], label='specific')
                    SG.add_edge(r['id'], r['targetId'], label='general')
                else:
                    SG.add_edge(r['id'], r['sourceId'], label='source')
                    SG.add_edge(r['id'], r['targetId'], label='target')

                outfile.write(f"v {idx} {r['type']}\n")

            for u, v, data in SG.edges(data=True):
                outfile.write(f"e {id_to_idx[u]} {id_to_idx[v]} {data['label']}\n")

        graphs.append(SG)
        file_names.append(f"{m['archimateId']}.json")

    with open(os.path.join(output_dir, 'graphs.pickle'), 'wb') as f:
        pickle.dump(graphs, f)

    return [[i, graph] for i, graph in zip(file_names, graphs)]
        