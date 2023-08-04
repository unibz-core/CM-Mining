from gspan_mining.config import parser
from gspan_mining.main import main
import sys

def run_gspan(input):
    FLAGS, _ = parser.parse_known_args(args=input.split())
    file_name = 'input/outputpatterns.txt'
    try: 
        with open(file_name, 'a', encoding='utf-8') as my_file:
            sys.stdout = my_file
            gs = main(FLAGS)
        with open(file_name, 'r') as fd:
            data = fd.read()
            list_ = data.split("\n")
    finally:
        sys.stdout = sys.__stdout__ 

def gsparameters(values):
    i,j = values
    parameters = f'-s {i} -l {j} -d False -v False -p False -w True ./input/graphs.data'
    return parameters

# #python -m gspan_mining [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d True/False] [-v True/False] [-p True/False] [-w True/False] [-h] database_file_name 

# if __name__ == '__main__':
#     #args_str = '-s 10 -l 5 -d False -v False -p False -w True ./input/fullundirected.data' #ok dots-asso
#     input = '-s 35 -l 5 -d False -v False -p False -w True ./input/graphs.data' #ok dots-asso
#     run_gspan(input)

#https://gitlab.inria.fr/Quickspan/quickspan/-/tree/master/extern/data
