import os, pickle
import networkx as nx
from pathlib import Path

def create_graph(models: list[dict], output_dir: Path) -> list:
    graphs = []
    gspan_output_file = os.path.join(output_dir, 'graphs.data')
    with open(gspan_output_file, 'w'):
        # create empty file
        pass
    
    for i, m in enumerate(models):
        # create a new subgraph for each model
        SG = nx.Graph(directed=True)
        with open(gspan_output_file, 'a') as outfile:
            outfile.write(f"t # {i} {m['name']}\n")
            
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

    with open(os.path.join(output_dir, 'graphs.pickle'), 'wb') as f:
        pickle.dump(graphs, f)

    return graphs
        