"""
This module provides a comprehensive set of functions for generating NetworkX graphs from JSON data files that describe
various aspects of a system's structure and relationships. These functions enable users to extract class information,
associations, generalizations, generalization sets, and other essential components from JSON files and represent them
as interconnected graphs using the NetworkX library.
"""


import json
from itertools import tee

import jsonpath_rw_ext as jp
import networkx as nx

extension = '.json'  # replace with the desired file extension

def get_classes(x, directory_path):
    """
    Retrieve class information from JSON files.

    :param x: List of JSON file names.
    :type x: list
    :param directory_path: Path to the directory containing the OntoUML models in JSON format to be converted.
    :type directory_path: str

    :return: List of tuples containing class data.
    :rtype: list
    """
    class_output = []
    for file_name in x:
        file = open(directory_path + "/" + file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        class_name = jp.match('$..contents[?(@.type=="Class")].name', data)
        # stereotype_name = jp.match('$..contents[?(@.type=="Class")].stereotype', data)
        stereotype_name = [item if item is not None else 'class' for item in
                           jp.match('$..contents[?(@.type=="Class")].stereotype', data)]
        id = jp.match('$..contents[?(@.type=="Class")].id', data)
        restrictionList = jp.match('$..contents[?(@.type=="Class")].restrictedTo', data)
        zipped = list(zip(id, class_name, stereotype_name, restrictionList))
        class_output.append(zipped)
    return class_output


def get_generalizations(x,directory_path):
    """
    Retrieve generalization relationships from JSON files.

    :param x: List of JSON file names.
    :type x: list
    :param directory_path: Path to the directory containing the OntoUML models in JSON format to be converted.
    :type directory_path: str

    :return: List of tuples containing generalization data.
    :rtype: list
    """
    gen_output = []
    for file_name in x:
        file = open(directory_path + "/" + file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        gen = jp.match('$..general.id', data)
        spec = jp.match('$..specific.id', data)
        genID = jp.match('$..contents[?(@.type=="Generalization")].id', data)
        zipped = list(zip(genID, gen, spec))
        gen_output.append(zipped)
    return gen_output


def get_associations(x,directory_path):
    """
    Retrieve association details from JSON files.

    :param x: List of JSON file names.
    :type x: list
    :param directory_path: Path to the directory containing the OntoUML models in JSON format to be converted.
    :type directory_path: str

    :return: List of tuples containing association data.
    :rtype: list
    """
    association_output = []
    for file_name in x:
        file = open(directory_path + "/" + file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        # association_name = jp.match('$..contents[?(@.type=="Relation")].name', data)
        association_name = [name if name else 'empty' for name in
                            jp.match('$..contents[?(@.type=="Relation")].name', data)]
        stereotype_name = [name if name else 'relation' for name in
                           jp.match('$..contents[?(@.type=="Relation")].stereotype', data)]
        id = jp.match('$..contents[?(@.type=="Relation")].id', data)
        cardinalities = [item for item in jp.match('$..properties[?(@.cardinality)].cardinality', data) if
                         item is not None]
        # coupled_cardinalities = [cardinalities[n:n+2] for n in range(0, len(cardinalities), 2)]
        coupled_cardinalities = [[cardinalities[n], cardinalities[n + 1] if n + 1 < len(cardinalities) else 'Empty'] for
                                 n in range(0, len(cardinalities), 2)]
        source_target0 = [item for item in jp.match('$..contents[?(@.type=="Relation")]', data) if item is not None]
        source_target1 = jp.match('$..propertyType.id', source_target0)
        coupled_source_target = [source_target1[n:n + 2] for n in range(0, len(source_target1), 2)]
        zipped = [(a, str(b), str(c), d, *e) for a, b, c, d, e in
                  zip(id, association_name, stereotype_name, coupled_cardinalities, coupled_source_target)]
        association_output.append(zipped)
    return association_output


def get_genset(x,directory_path):
    """
    Retrieve generalization set information from JSON files.

    :param x: List of JSON file names.
    :type x: list
    :param directory_path: Path to the directory containing the OntoUML models in JSON format to be converted.
    :type directory_path: str

    :return: List of tuples containing generalization set data.
    :rtype: list
    """
    gen_set_output = []
    for file_name in x:
        file = open(directory_path + "/" + file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        id = jp.match('$..contents[?(@.type=="GeneralizationSet")].id', data)
        disj = jp.match('$..contents[?(@.type=="GeneralizationSet")].isDisjoint', data)
        comp = jp.match('$..contents[?(@.type=="GeneralizationSet")].isComplete', data)
        name = jp.match('$..contents[?(@.type=="GeneralizationSet")].name', data)
        gen_ids = [jp.match('$..generalizations[?(@.id)].id', i) for i in
                   jp.match('$..contents[?(@.type=="GeneralizationSet")]', data)]
        # zipped = [(a,'isComplete:'+str(b),'isDisjoint:'+str(c),str(d),*e) for a,b,c,d,e in zip(id,disj,comp,name,gen_ids)] unfold set of ids
        zipped = [(a, str(b), str(c), str(d), e) for a, b, c, d, e in zip(id, disj, comp, name, gen_ids)]
        gen_set_output.append(zipped)
    return gen_set_output


def get_restrictedTo(x,directory_path):
    """
    Retrieve "restricted to" information for classes from JSON files.

    :param x: List of JSON file names.
    :type x: list
    :param directory_path: Path to the directory containing the OntoUML models in JSON format to be converted.
    :type directory_path: str

    :return: List of tuples containing restrictedTo data.
    :rtype: list
    """
    gen_set_output = []
    for file_name in x:
        file = open(directory_path + "/" + file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        restrictionList = jp.match('$..contents[?(@.type=="Class")].restrictedTo', data)
        id_list = jp.match('$..contents[?(@.type=="Class")].id', data)

        output_list = []
        for i in range(len(id_list)):
            current_id = id_list[i]
            if restrictionList[i] is not None:
                for item in restrictionList[i]:
                    output_list.append((current_id, item))
            else:
                output_list.append((current_id, 'None'))

        gen_set_output.append(output_list)

    return gen_set_output


def pairwise(iterable):
    """
    Iterate through pairs of items in an iterable.

    :param iterable: Iterable to be paired.
    :type iterable: iterable

    :return: A zip object containing pairs of items.
    :rtype: zip
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_genset_rel(x):
    """
    Generate relationships for generalization sets and their components.

    :param x: List of generalization set data.
    :type x: list

    :return: List of lists containing relationships.
    :rtype: list
    """
    list_ = []
    for i in x:
        gens = [(a, *e) for a, b, c, d, e in i]
        result = [list(map(lambda x: (i[0], x[1]), pairwise(i))) for i in gens]
        list_.append(result)
    return list_


# %%

def create_FullUndirectedGraphs(file_names, nodesA, nodesB, nodesC, nodesD, nodesE, nodesF, nodesG, nodesH, edgesA,
                                edgesB, edgesC, edgesD, edgesE, edgesF, edgesG, edgesH, edgesI, edgesY):
    """
    Create NetworkX graphs from data.

    :param file_names: List of file names.
    :type file_names: list
    :param nodesA, nodesB, ..., edgesY: Data lists for nodes and edges.

    :return: List of tuples containing file names and NetworkX graphs.
    :rtype: list
    """
    graphs = []

    for file_name, node_list_A, node_list_B, node_list_C, node_list_D, node_list_E, node_list_F, node_list_G, node_list_H, edge_list_A, edge_list_B, edge_list_C, edge_list_D, edge_list_E, edge_list_F, edge_list_G, edge_list_H, edge_list_I, edge_list_Y in zip(
            file_names, nodesA, nodesB, nodesC, nodesD, nodesE, nodesF, nodesG, nodesH, edgesA, edgesB, edgesC, edgesD,
            edgesE, edgesF, edgesG, edgesH, edgesI, edgesY):
        # Create an empty graph
        G = nx.Graph()

        # Add nodes to the graph
        for node_data in node_list_A:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_B:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_C:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_D:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_E:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_F:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_G:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)
        for node_data in node_list_H:
            node_labels = {'label': node_data[1]}
            node_labels.update({f'label{i}': label for i, label in enumerate(node_data[2:])})
            G.add_node(node_data[0], **node_labels)

        # Add edges to the graph
        for edge_data in edge_list_A:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_B:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_C:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_D:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_E:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_F:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_G:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_H:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_I:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)
        for edge_data in edge_list_Y:
            edge_labels = {'label': edge_data[2]}
            edge_labels.update({f'label{i}': label for i, label in enumerate(edge_data[3:])})
            G.add_edge(edge_data[0], edge_data[1], **edge_labels)

        graphs.append(G)

    return graphs


# %%

def generateFullUndirected(file_names):
    """
    Generate full undirected graphs from data.

    :param file_names: List of file names.
    :type file_names: list

    :return: List of tuples containing file names and NetworkX graphs.
    :rtype: list
    """
    classes = get_classes(file_names)
    generalizations = get_generalizations(file_names)
    associations = get_associations(file_names)
    genset = get_genset(file_names)
    restrictedTo = get_restrictedTo(file_names)
    genset_rel = [sum(i, []) for i in get_genset_rel(genset)]
    associations_cardinalities_v = [[("0" + str(d).replace(" ", "").replace("'", "").replace(",", "_").replace('[',
                                                                                                               '').replace(
        ']', '').replace('.', '') + "_", str(d).replace(" ", "").replace("'", "").replace(",", "_").replace('[',
                                                                                                            '').replace(
        ']', '').replace('.', '')) for a, b, c, d, e, f in i] for i in associations]
    geneset_disjoint_v = [[("0" + str(b).replace(" ", "").replace("'", "").replace(",", "_").replace('[', '').replace(
        ']', '').replace('.', '') + "_", str(b)) for a, b, c, d, e in i] for i in genset]
    geneset_complete_v = [[("0" + str(c).replace(" ", "").replace("'", "").replace(",", "_").replace('[', '').replace(
        ']', '').replace('.', '') + "_", str(c)) for a, b, c, d, e in i] for i in genset]
    classes_v = [
        [(str(a), str(c).replace(" ", "-").replace(":", "-"), str(b).replace(" ", "-").replace(":", "-")) for a, b, c, d
         in i] for i in classes]
    generalizations_v = [[(a, "gen") for a, b, c in i] for i in generalizations]
    associations_v = [[(a, str(c).replace(" ", "-").replace(":", "-"), str(b).replace(" ", "-").replace(":", "-")) for
                       a, b, c, d, e, f in i] for i in associations]
    geneset_v = [[(str(a), "gen-set") for a, b, c, d, e in i] for i in genset]
    restrictedTo_v = [[("0" + str(b).replace(" ", "").replace("'", "").replace(",", "_").replace('[', '').replace(']',
                                                                                                                  '').replace(
        '.', '').replace('-', '') + "_", str(b).replace('-', '')) for a, b in i] for i in restrictedTo]

    generalizations_general_e = [[(b, a, "general") for a, b, c in i] for i in generalizations]
    generalizations_specific_e = [[(c, a, "specific") for a, b, c in i] for i in generalizations]
    associations_source_e = [[(str(e), str(a), "source") for a, b, c, d, e, f in i] for i in associations]
    associations_target_e = [[(str(f), str(a), "target") for a, b, c, d, e, f in i] for i in associations]
    associations_cardinalities_e = [[(str(x), str(a), "cardinalities")
                                     for x, y in k for a, b, c, d, e, f in i] for i, k in
                                    zip(associations, associations_cardinalities_v)]
    geneset_disjoint_e = [[(str(x), str(a), "isDisjoint")
                           for x, y in k for a, b, c, d, e in i] for i, k in zip(genset, geneset_disjoint_v)]
    geneset_complete_e = [[(str(x), str(a), "isComplete")
                           for x, y in k for a, b, c, d, e in i] for i, k in zip(genset, geneset_complete_v)]
    genset_e = [[(str(b), str(a), "generalization") for a, b in i] for i in genset_rel]
    restrictedTo_e = [[(a,
                        "0" + str(b).replace(" ", "").replace("'", "").replace(",", "_").replace('[', '').replace(']',
                                                                                                                  '').replace(
                            '.', '').replace('-', '') + "_", "restrictedTo") for a, b in i] for i in restrictedTo]

    graphs = create_FullUndirectedGraphs(file_names, associations_cardinalities_v, geneset_disjoint_v,
                                         geneset_complete_v, classes_v, generalizations_v, associations_v, geneset_v,
                                         restrictedTo_v,
                                         generalizations_general_e, generalizations_specific_e, associations_source_e,
                                         associations_target_e, associations_target_e, associations_cardinalities_e,
                                         geneset_disjoint_e, geneset_complete_e, genset_e, restrictedTo_e)
    # return graphs
    return [[i, graph] for i, graph in zip(file_names, graphs)]
