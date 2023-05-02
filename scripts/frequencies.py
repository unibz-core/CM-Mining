import networkx as nx
from itertools import groupby
from grandiso import find_motifs
import os
import networkx as nx
import matplotlib.pyplot as plt
from textwrap import wrap
import numpy as np
from matplotlib import rcParams

fd = open("output.txt", "r+")
# sys.stdout = sys.__stdout__
data = fd.read()
list_ = data.split("\n")
fd.close()


####Generate NetworkX Graphs from patterns
ele = '-----------------' 
# Group strings at particular element in list
# using groupby() + list comprehension + lambda
res = [list(j) for i, j in groupby(list_, lambda x:x == ele) if not i]

out = [[k for k in w if 'Support:' not in k] for w in res]
out0 = [[k for k in w if 't #' not in k] for w in out]
out1 = [[k for k in w if 'Read:' not in k] for w in out0]
out2 = [[k for k in w if 'Mine:' not in k] for w in out1]
out3 = [[k for k in w if 'Total:' not in k] for w in out2]
out4 = [[s for s in sub_list if s] for sub_list in out3]
final_list = list(filter(None, out4))
#print("Resultant patterns list after grouping : " + str(final_list))
#print(final_list)

pattern_graphs = []
for sublist in final_list:
    # Create a new graph
    G = nx.Graph()
    #G0 = G.to_directed()
    # Iterate over each item in the sublist
    for item in sublist:
        # If the item is a node, add it to the graph
        if item.startswith('v'):
            node_id, node_label = item.split()[1:]
            G.add_node(node_id, label=node_label)
        # If the item is an edge, add it to the graph
        elif item.startswith('e'):
            target, source, edge_label = item.split()[1:]
            G.add_edge(source, target, label=edge_label)
    # Append the graph to the list of graphs
    pattern_graphs.append(G)

####Generate NetworkX Graphs from graphs
#### input graphs
fi = open("./input/test.data", "r+")
#sys.stdout = sys.__stdout__
data = fi.read()
list__ = data.split("\n")
fi.close()

new_list = ['###' if 't #' in item else item for item in list__]
from itertools import groupby
ele_ = '###' 
res_ = [list(j) for i, j in groupby(new_list, lambda x:x == ele_) if not i]
out0__ = [[k for k in w if '###' not in k] for w in res_]
out1__ = [[s for s in sub_list if s] for sub_list in out0__]
final_list0 = list(filter(None, out1__))

source_graphs = []
for sublist in final_list0:
    # Create a new graph
    K = nx.Graph()
    # Iterate over each item in the sublist
    for item in sublist:
        # If the item is a node, add it to the graph
        if item.startswith('v'):
            node_id, node_label = item.split()[1:]
            K.add_node(node_id, label=node_label)
        # If the item is an edge, add it to the graph
        elif item.startswith('e'):
            target, source, edge_label = item.split()[1:]
            K.add_edge(source, target, label=edge_label)
    # Append the graph to the list of graphs
    source_graphs.append(K)

# for i in source_graphs:
#     print("Sources :")
#     print(i)
#     #print("Source :"+str(i.edges(data=True)))
#     print("Sources :"+str(i.nodes(data=True)))

#https://github.com/aplbrain/grandiso-networkx


def count_subgraph_isomorphisms(source_graphs, target_graphs):
    #Initialize a dictionary to keep track of the counts for each input graph
    count_dict = {i: [0] * len(target_graphs) for i in range(len(source_graphs))}
    # Loop through each source graph and target graph
    for i, source_graph in enumerate(source_graphs):
        for j, target_graph in enumerate(target_graphs):
            # Use find_motifs to find matches
            matches = find_motifs(source_graph, target_graph) #directed=True)
            # print(matches)
            filtered_matches = [sub['0'] for sub in matches]
            count_dict[i][j] = len(list(dict.fromkeys(filtered_matches)))
    # Update count_dict to have values indexed from 0 to n
    for key in count_dict:
        count_dict[key] = dict(enumerate(count_dict[key]))
    return count_dict

models_count = count_subgraph_isomorphisms(pattern_graphs,source_graphs)
models_count0_ = [{k:v} for k, v in models_count.items()]

def filter_zero_values(input_dicts):
    for d in input_dicts:
        for k, v in d.items():
            d[k] = {k1: v1 for k1, v1 in v.items() if v1 != 0}
    return input_dicts

models_count0 = filter_zero_values(models_count0_)

# for i in models_count0:
#     print("Models Count:")
#     # print(i)

list_of_dics = [{k:v} for k, v in models_count.items()]
def overall_frequency(input_dicts):
    output_dict = {}
    for input_dict in input_dicts:
        for key, sub_dict in input_dict.items():
            if key not in output_dict:
                output_dict[key] = sum(sub_dict.values())
            else:
                output_dict[key] += sum(sub_dict.values())
    return output_dict

# input_dicts = [{0: {0: 0, 1: 1, 2: 1}, 1: {0: 0, 1: 1, 2: 3}}]
overall = overall_frequency(list_of_dics)
overall0 = [{k:v} for k, v in overall.items()]
# print("Oveall Frequencies:")
# print(overall0)  # Output: {0: 2, 1: 4}

list_of_dics0 = [{k:v} for k, v in models_count.items()]
def count_nonzero_values(input_dicts):
    output_list = []
    for input_dict in input_dicts:
        count_dict = {}
        for key in input_dict:
            count_dict[key] = sum(1 for value in input_dict[key].values() if value != 0)
        output_list.append(count_dict)
    return output_list

#input_dicts = [{0: {0: 0, 1: 1, 2: 1}, 1: {0: 0, 1: 1, 2: 3}}]

models_freq = count_nonzero_values(list_of_dics0)
# print("Models Frequencies:")
# print(models_freq)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) #pydot

def visualize_graphs(graphs, subtitles):
    assert len(graphs) == len(subtitles), "Number of graphs and subtitles must be the same"

    if not os.path.exists('dots'):
        os.makedirs('dots')

    for i, graph in enumerate(graphs):
        fig, ax = plt.subplots(figsize=(6, 6))
        pos = nx.nx_pydot.graphviz_layout(graph, prog='dot') 
        #pos = nx.nx_agraph.graphviz_layout(graph, prog='dot') 
        # Rotate the graph layout by 90 or 180 degrees
        #pos = {k: (v[1], -v[0]) for k, v in pos.items()}
        pos = {k: (-v[0], -v[1]) for k, v in pos.items()}
        #nx.draw(graph, pos, with_labels=False, connectionstyle='arc3, rad = 0.3', font_size=10, font_weight='bold',node_color='b', alpha=0.2)
        nx.draw(graph, pos, with_labels=False, font_size=10, font_weight='bold',node_color='b', alpha=0.2)
        nlabels = nx.get_node_attributes(graph, 'label')
        elabels = nx.get_edge_attributes(graph, 'label')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=elabels, font_size=7, font_weight='bold')
        nx.draw_networkx_labels(graph, pos, labels=nlabels, font_size=7, font_weight='bold')
        # Set the title with white margins on both sides
        ax.set_title(subtitles[i], fontsize=7, loc='center', wrap=True, pad=12, color='black', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.4'))
        # Add white margins on both sides of the plot
        fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.83, wspace=0.3, hspace=0.3)
        plt.savefig(f'dots/graph_{i}.png', dpi=300, bbox_inches=None)
        plt.close()

    plt.show()

stat_zip = list(zip(models_freq,overall0,models_count0))
visualize_graphs(pattern_graphs,stat_zip)

#other tests

# def visualize_graphs(graphs, subtitles):
#     assert len(graphs) == len(subtitles), "Number of graphs and subtitles must be the same"

#     if not os.path.exists('dots'):
#         os.makedirs('dots')

#     for i, graph in enumerate(graphs):
#         fig, ax = plt.subplots(figsize=(6, 6))
#         pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
#         nx.draw(graph, pos, with_labels=False, font_size=10, font_weight='bold')
#         nlabels = nx.get_node_attributes(graph, 'label')
#         elabels = nx.get_edge_attributes(graph, 'label')
#         nx.draw_networkx_edge_labels(graph, pos, edge_labels=elabels, font_size=7, font_weight='bold')
#         nx.draw_networkx_labels(graph, pos, labels=nlabels, font_size=7, font_weight='bold')
#         ax.set_title(subtitles[i], fontsize=7, loc='center', wrap=True, size=6)
#         fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9, wspace=0.3, hspace=0.3)
#         plt.savefig(f'dots/graph_{i+1}.png', dpi=300, bbox_inches=None) #pad_inches=0.9)
#         plt.close()

#     plt.show()


# def visualize_graphs(graphs, subtitles):
#     assert len(graphs) == len(subtitles), "Number of graphs and subtitles must be the same"

#     if not os.path.exists('dots'):
#         os.makedirs('dots')

#     for i, graph in enumerate(graphs):
#         fig, ax = plt.subplots(figsize=(10, 6))
#         pos = nx.nx_pydot.graphviz_layout(graph, prog='dot')
#         #pos = {k: (v[1], -v[0]) for k, v in pos.items()} # reverse the y-axis for a top-down tree
#         nx.draw(graph, pos, with_labels=False, font_size=10, font_weight='bold')
#         nlabels = nx.get_node_attributes(graph, 'label')
#         elabels = nx.get_edge_attributes(graph, 'label')
#         nx.draw_networkx_edge_labels(graph, pos, edge_labels=elabels, font_size=10, font_weight='bold')
#         nx.draw_networkx_labels(graph, pos, labels=nlabels, font_size=10, font_weight='bold')
#         ax.set_title(subtitles[i], fontsize=10, loc='center', pad=20, wrap=True)
#         ax.set_xlabel('', fontsize=8)
#         ax.set_ylabel('', fontsize=8)
#         plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)
#         plt.savefig(f'dots/graph_{i+1}.png', dpi=300, bbox_inches='tight')
#         plt.close()

#     plt.show()



#pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']


# import os
# import networkx as nx
# from networkx.drawing.nx_pydot import write_dot

# stat_zip = list(zip(models_freq,overall0,models_count0))


# def write_dot_files(graph_list):
#     # Create a directory to store the dot files
#     os.makedirs("dots", exist_ok=True)
    
#     # Iterate over the list of graphs and write a dot file for each graph
#     for i, graph in enumerate(graph_list):
#         file_name = f"dots/{i}.txt"
#         write_dot(graph, file_name)

# write_dot_files(pattern_graphs)

# # # loop through the directory and get file names with the desired extension
# directory_path = './dots'  # replace with the path to your directory
# extension = '.pdf'  # replace with the desired file extension
# dot_files = []
# for filename in os.listdir(directory_path):
#     if filename.endswith(extension):
#         dot_files.append(filename)
# # 
# print(dot_files)

# import glob
# for file in glob.glob("dots/"+'*txt'):
#     with open(file.replace('.txt', '_.txt'), 'w') as outfile:
#         with open(file) as infile:
#             text = infile.readlines()
#             text.insert(1, "rankdir=BT;\n")
#             outfile.write(''.join(text))

# outpath = "./dots/"
# my_dir = outpath
# for fname in os.listdir(outpath):
#     if not fname.endswith("_.txt"):
#         os.remove(os.path.join(my_dir, fname))
        
# # # # #visualization
# from graphviz import Source
# for r in os.listdir(outpath):
#     if r.endswith('.txt'):
#         f = os.path.join(outpath, r)
#         g = nx.drawing.nx_agraph.read_dot(f)
#         s = Source.from_file(f)
#         s.render() #convert - pdf





# pdfs = './dots'  # replace with the path to your directory
# extension = '.pdf'  # replace with the desired file extension

# # loop through the directory and get file names with the desired extension
# file_names = []
# for filename in os.listdir(pdfs):
#     if filename.endswith(extension):
#         file_names.append(filename)



# from pypdf import PdfMerger

# pdfs = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf']

# merger = PdfMerger()

# for pdf in pdfs:
#     merger.append(pdf)

# merger.write("result.pdf")
# merger.close()








#python3 -m pip install 'PyPDF2<3.0'
#report
# #captions = ["Caption 1", "Caption 2", "Caption 3"] # Replace with your own list of captions

# import os
# import io 
# from reportlab.pdfgen import canvas
# from PyPDF2 import PdfFileWriter, PdfFileReader

# def create_visualized_pdfs(pdf_files, items):
#     output_files = []
#     for i, pdf_file in enumerate(pdf_files):
#         item = items[i]
#         input_pdf = PdfFileReader(open(outpath+pdf_file, "rb"))
#         output_pdf = PdfFileWriter()

#         for page_num in range(input_pdf.getNumPages()):
#             # create a new PDF page
#             packet = io.BytesIO()
#             can = canvas.Canvas(packet)

#             # add the item to the PDF page
#             can.drawString(100, 720, item)
#             can.drawString(100, 700, os.path.basename(pdf_file))

#             can.save()

#             # move to the beginning of the StringIO buffer
#             packet.seek(0)
#             new_pdf_page = PdfFileReader(packet).getPage(0)

#             # merge the PDF page with the input PDF page
#             input_page = input_pdf.getPage(page_num)
#             input_page.mergePage(new_pdf_page)
#             output_pdf.addPage(input_page)

#         # create a new output PDF file
#         output_file_path = os.path.splitext(pdf_file)[0] + "_visualized.pdf"
#         with open(output_file_path, "wb") as output_file:
#             output_pdf.write(output_file)

#         output_files.append(output_file_path)

#     return output_files

# captions = ["Caption 1", "Caption 2", "Caption 3", "Caption 4"] 
# create_visualized_pdfs(dot_files,captions)