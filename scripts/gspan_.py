
#conda create -n chatbot_env
#conda activate chatbot_env
#conda install diffusers transformers accelerate xformers hvplot panel notebook -c pytorch -c conda-forge

#conda config --append channels conda-forge
#conda install pandas==0.18

# conda config --append channels conda-forge
# conda install gspan-mining

# '/Users/mattia/opt/anaconda3/envs/mining-env/bin/pip' install gspan-mining  

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)
# import pandas as pd


########
#check the differences between a graph and a pattern

# help python3 -m gspan_mining -h
# https://github.com/betterenvi/gSpan
from gspan_mining.config import parser
from gspan_mining.main import main

#You can increase/decrease the available RAM for VS Code on its Settings. 
# Go to File -> Preferences -> Settings, there you can type files.maxMemoryForLargeFilesMB and change the value for your desired maximum RAM.

#args_str = '-s 13 -n 200 -l 3 -u 10 -d True -v False -p False -w True ./input/items0.data' #ok 198.97 s
#args_str = '-s 12 -n 200 -l 3 -u 10 -d True -v False -p False -w True ./input/items0.data' #ok 175.05 s
#args_str = '-s 32  -n 140 -l 5 -u 15 -d False -v False -p False ./input/complex.data' #ok

#args_str = '-s 25  -n 100 -l 5 -u 20 -d False -v False -p False ./input/complex.data' #ok dots-gen-asso
#args_str = '-s 12 -n 150 -l 5 -u 25 -d False -v False -p False ./input/complex.data' #ok dots-asso
args_str = '-s 2 -n 150 -l 3 -u 25 -d False -v False -p False ./input/test.data' #ok dots-asso

#python -m gspan_mining [-s min_support] [-n num_graph] [-l min_num_vertices] [-u max_num_vertices] [-d True/False] [-v True/False] [-p True/False] [-w True/False] [-h] database_file_name 
FLAGS, _ = parser.parse_known_args(args=args_str.split())
# Example usage
import sys
file_name = 'output.txt'
with open(file_name, 'w', encoding='utf-8') as my_file:
    sys.stdout = my_file
    gs = main(FLAGS)
fd = open("output.txt", "r+")
# sys.stdout = sys.__stdout__
data = fd.read()
list_ = data.split("\n")
fd.close()

