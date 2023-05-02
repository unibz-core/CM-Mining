#from application.app.folder.file import func_name
#https://pypi.org/project/jsonpath-rw-ext/
#https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html
#https://rungutan.com/blog/extract-value-json-path-expression/
#https://github.com/Patimir/yt-notebooks/blob/main/Creating_RDF_triples.ipynb

# from time import sleep
# from tqdm import tqdm
# for i in tqdm(range(100)):
import os
import glob
import json
import jsonpath_rw_ext as jp
from itertools import chain
from functools import reduce

import os
directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension

# loop through the directory and get file names with the desired extension
file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)



# %%

def get_classes(x):
    class_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        class_name = jp.match('$..contents[?(@.type=="Class")].name', data)
        stereotype_name = jp.match('$..contents[?(@.type=="Class")].stereotype', data)
        id = jp.match('$..contents[?(@.type=="Class")].id', data)
        zipped = list(zip(id,class_name,stereotype_name))
        class_output.append(zipped)
    return class_output

def get_generalizations(x):
    gen_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        gen = jp.match('$..general.id', data)
        spec = jp.match('$..specific.id', data)
        genID = jp.match('$..contents[?(@.type=="Generalization")].id', data)
        zipped = list(zip(genID,gen,spec))
        gen_output.append(zipped)
    return gen_output

def get_associations(x):
    association_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        association_name = jp.match('$..contents[?(@.type=="Relation")].name', data)
        stereotype_name = jp.match('$..contents[?(@.type=="Relation")].stereotype', data)
        id = jp.match('$..contents[?(@.type=="Relation")].id', data)
        cardinalities = [item for item in jp.match('$..properties[?(@.cardinality)].cardinality', data) if item is not None]
        coupled_cardinalities = [cardinalities[n:n+2] for n in range(0, len(cardinalities), 2)]
        source_target0 = [item for item in jp.match('$..contents[?(@.type=="Relation")]', data) if item is not None]
        source_target1 = jp.match('$..propertyType.id', source_target0)
        coupled_source_target = [source_target1[n:n+2] for n in range(0, len(source_target1), 2)]
        zipped = [(a,str(b),str(c),d,*e) for a,b,c,d,e in zip(id,association_name,stereotype_name,coupled_cardinalities,coupled_source_target)]
        association_output.append(zipped)
    return association_output

def get_genset(x):
    gen_set_output = []
    for file_name in x:
        file = open(directory_path+"/"+file_name, encoding="ISO-8859-1", mode="r")
        data = json.loads(file.read())
        id = jp.match('$..contents[?(@.type=="GeneralizationSet")].id', data)
        disj = jp.match('$..contents[?(@.type=="GeneralizationSet")].isDisjoint', data)
        comp = jp.match('$..contents[?(@.type=="GeneralizationSet")].isComplete', data)
        name = jp.match('$..contents[?(@.type=="GeneralizationSet")].name', data)
        gen_ids = [jp.match('$..generalizations[?(@.id)].id', i) for i in jp.match('$..contents[?(@.type=="GeneralizationSet")]', data)]
        #zipped = [(a,'isComplete:'+str(b),'isDisjoint:'+str(c),str(d),*e) for a,b,c,d,e in zip(id,disj,comp,name,gen_ids)] unfold set of ids
        zipped = [(a,str(b),str(c),str(d),e) for a,b,c,d,e in zip(id,disj,comp,name,gen_ids)]
        gen_set_output.append(zipped)
    return gen_set_output

from itertools import combinations
#https://www.geeksforgeeks.org/python-all-possible-pairs-in-list/
from itertools import tee

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def get_genset_rel(x):
    list_ = []
    for i in x:
        gens = [(a,*e) for a,b,c,d,e in i]
        result = [list(map(lambda x: (i[0], x[1]), pairwise(i))) for i in gens]
        list_.append(result)
    return list_

# %%

classes = get_classes(file_names)
generalizations = get_generalizations(file_names)
associations = get_associations(file_names)
genset = get_genset(file_names)
genset_rel = [sum(i, []) for i in get_genset_rel(genset)]
for i in associations:
    print(i)
# print(genset)
# print(genset_rel)

# %%

def create_gspan_input(file_names):
    file = open('./input/test.data','w')
    index = 0
    for x,y,z,w,j,k in zip(file_names,classes,generalizations,associations,genset,genset_rel):
        file.write("t"+" "+"#"+" "+"{}".format(str(index)+" "+x).replace('.json','')+"\n")
        index += 1
    #nodes
        classes_v = [("v"+" "+str(a)+" "+str(c).replace(" ", "")) for a,b,c in y]
        classes_name = [("v"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(b).replace(" ", "")+"_v") for a,b,c in y] #check characters
        #classes_stereotype = [("v"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(c).replace(" ", "")) for a,b,c in y]
        generalizations_v = [("v"+" "+str(a)+" "+"gen") for a,b,c in z]
        associations_v = [("v"+" "+str(a)+" "+str(c).replace(" ", "")) for a,b,c,d,e,f in w]
        associations_name = [("v"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(b).replace(" ", "")+"_v") for a,b,c,d,e,f in w] #check characters
        #associations_stereotype = [("v"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(c).replace(" ", "")) for a,b,c,d,e,f in w]
        associations_cardinalities = [("v"+" "+"0"+str(d).replace(" ", "")+"_"+" "+str(d).replace(" ", "")) for a,b,c,d,e,f in w]
        geneset_v = [("v"+" "+str(a)+" "+"gen-set") for a,b,c,d,e in j]
        geneset_disjoint = [("v"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(b)) for a,b,c,d,e in j]
        geneset_complete = [("v"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(c)) for a,b,c,d,e in j]
    #edges
        generalizations_general = [("e"+" "+str(b)+" "+str(a)+" "+"general") for a,b,c in z]
        generalizations_specific = [("e"+" "+str(c)+" "+str(a)+" "+"specific") for a,b,c in z]
        classes_name_e = [("e"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(a)+" "+"name") for a,b,c in y]
        #classes_stereotype_e = [("e"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(a)+" "+"isStereotype") for a,b,c in y]
        associations_name_e = [("e"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(a)+" "+"name") for a,b,c,d,e,f in w]
        #associations_stereotype_e = [("e"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(a)+" "+"isStereotype") for a,b,c,d,e,f in w]
        associations_cardinalities_e = [("e"+" "+"0"+str(d).replace(" ", "")+"_"+" "+str(a)+" "+"cardinalities") for a,b,c,d,e,f in w]
        associations_source = [("e"+" "+str(e)+" "+str(a)+" "+"source") for a,b,c,d,e,f in w]
        associations_target = [("e"+" "+str(f)+" "+str(a)+" "+"target") for a,b,c,d,e,f in w]
        genset_e = [("e"+" "+str(b)+" "+str(a)+" "+"generalization") for a,b in k]
        geneset_disjoint_e = [("e"+" "+"0"+str(b).replace(" ", "")+"_"+" "+str(a)+" "+"isDisjoint") for a,b,c,d,e in j]
        geneset_complete_e = [("e"+" "+"0"+str(c).replace(" ", "")+"_"+" "+str(a)+" "+"isComplete") for a,b,c,d,e in j]
    #nodes
        for i in classes_v:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        # for i in classes_name:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', ''),('Ã ', 'A'),('Ã', 'A'),('³', ''),('ª', ''),('¢', ''),('£', ''),('©', ''),('º', ''),('A¡rio', 'Airio'),('A¡fe', 'Aife'),('A','A'),('::',''),('-',''),('/',''),('§',''),(':',''),('\n','')      
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i).encode('utf-8', errors='ignore').decode('utf-8'))
        #     file.write(i0+"\n")
        for i in generalizations_v:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        for i in associations_v:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        # for i in associations_name:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', ''),('Ã ', 'A'),('Ã', 'A'),('³', ''),('ª', ''),('¢', ''),('£', ''),('©', ''),('º', ''),('A¡rio', 'Airio'),('A¡fe', 'Aife'),('A','A'),('::',''),('-',''),('/',''),('§',''),(':',''),('\n','')       
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i).encode('utf-8', errors='ignore').decode('utf-8'))
        #     file.write(i0+"\n")
        # for i in associations_cardinalities:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in geneset_v:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in geneset_disjoint:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in geneset_complete:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
    #edges
        for i in generalizations_general:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        for i in generalizations_specific:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        # for i in classes_name_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', ''),('Ã ', 'A'),('Ã', 'A'),('³', ''),('ª', ''),('¢', ''),('£', ''),('©', ''),('º', ''),('A¡rio', 'Airio'),('A¡fe', 'Aife'),('A','A'),('::',''),('-',''),('/',''),('§',''),(':',''),('\n','')      
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in associations_name_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in associations_cardinalities_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        for i in associations_source:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        for i in associations_target:
            repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
            i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
            file.write(i0+"\n")
        # for i in genset_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in geneset_disjoint_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
        # for i in geneset_complete_e:
        #     repls = ('(', ''), (')', ''), ("'", ""), (",", "_"), ('{', ''), ('}', ''), ('[', ''), (']', ''),('.', '') 
        #     i0 = reduce(lambda i, kv: i.replace(*kv), repls, str(i))
        #     file.write(i0+"\n")
    file.close()

doc = create_gspan_input(file_names)
    # sleep(3)

# %%



