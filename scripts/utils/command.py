from examples import custom_style_2
from PyInquirer import prompt, Separator
import os
import time
import utils.back2UML
import subprocess
import utils.generateinput
import utils.patterns 
import shutil
import utils.UMLviz
from prompt_toolkit.validation import Validator, ValidationError

directory_path = '../models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension
patternspath = "../input/outputpatterns.txt" # replace with patterns file name


def filterClasses():
    strings = ["class", "gen-set","kind", "subkind", "phase", "role", 
               "collective", "quantity", "relator", 
               "category", "phaseMixin", "roleMixin", 
               "mixin", "mode", "quality", "event", 
               "historicalRoleMixin", "historicalRole", 
               "situation", "type", "datatype", "enumeration"
               ]
    questions = [
        {
            'type': 'checkbox',
            'message': 'Select classes to filter-out:',
            'name': 'selected_strings',
            'choices': [
                {
                    'name': string
                }
                for string in strings
            ]
        }
    ]
    answers = prompt(questions,style=custom_style_2)
    selected_strings = answers['selected_strings']

    print("Deleted nodes (classes):", selected_strings)
    return selected_strings

def filterRelations():
    strings = ["relation", "gen","characterization", "comparative", "externalDependence", 
               "material", "mediation", "componentOf", "memberOf", 
               "subCollectionOf", "subQuantityOf", "bringsAbout", 
               "creation", "historicalDependence", "manifestation", 
               "participation", "participational", "termination", 
               "triggers", "instantiation"
               ]
    questions = [
        {
            'type': 'checkbox',
            'message': 'Select relations to filter-out:',
            'name': 'selected_strings',
            'choices': [
                {
                    'name': string
                }
                for string in strings
            ]
        }
    ]
    answers = prompt(questions,style=custom_style_2)
    selected_strings = answers['selected_strings']

    print("Deleted nodes (relations):", selected_strings)
    return selected_strings

def filterEdges():
    strings = ["cardinalities", "isComplete", "isDisjoint", "source", "target", "specific", "general", "generalization", "restrictedTo"]
    questions = [
        {
            'type': 'checkbox',
            'message': 'Select edges to filter-out:',
            'name': 'selected_strings',
            'choices': [
                {
                    'name': string
                }
                for string in strings
            ]
        }
    ]
    selected_strings = []
    while len(selected_strings) < 2:
        answers = prompt(questions,style=custom_style_2)
        selected_strings = answers['selected_strings']

        if len(selected_strings) < 2:
            print('\033[1;37;41mYou must choose at least two strings. Please try again.\033[0m\n' )
            time.sleep(2)

    print("Deleted edges:", selected_strings)
    return selected_strings


def count_files_in_folder(folder_path):
    file_count = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)
    return file_count

class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a value",
                                  cursor_position=len(document.text))

def parameters():
    questions = [
        {
            'type': "input",
            "name": "min_support",
            "message": "Enter the min_support value",
            "validate": NumberValidator,
            "filter": lambda val: int(val)
        },

        {
            'type': "input",
            "name": "min_num_vertices",
            "message": "Enter the min_num_vertices",
            "validate": NumberValidator,
            "filter": lambda val: int(val)
        }

    ]
    models = count_files_in_folder(directory_path)
    values = None
    
    while True:
        answers = prompt(questions,style=custom_style_2)
        min_support = answers['min_support']
        min_num_vertices = answers['min_num_vertices']
        values = [min_support, min_num_vertices]
        
        if min_support < 0.2 * models: #demo 0.4
            print("min_support should be at least 10 f models. Please try again.\n")
            continue
        
        break
    
    print("Selected values:", values)
    return values

def timeout_handler():
    print("Moving to the next function.")

def delete_files_in_folders(folders):
    for folder in folders:
        if os.path.exists(folder):
            # Delete all files within the folder
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            # Delete all subfolders within the folder
            for root, dirs, files in os.walk(folder, topdown=False):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    shutil.rmtree(dir_path)
        else:
            print(f"Folder '{folder}' does not exist.")

import sys
def firststop():
    # List of folders to delete files from
    folders = ["input","domaindots"]

    # Prompt to ask if the process is finished
    questions = [
        {
            'type': 'confirm',
            'name': 'finished',
            'message': 'Stop the process?',
            'default': False
        }
    ]
    answers = prompt(questions)

    if answers['finished']:
        # Ask for confirmation before deleting files
        confirm_question = [
            {
                'type': 'confirm',
                'name': 'confirm_delete',
                'message': 'Are you sure you want to delete all files in the folders?',
                'default': False
            }
        ]
        confirm_answer = prompt(confirm_question)
        if confirm_answer['confirm_delete']:
            delete_files_in_folders(folders)
            print("Files deleted. Process completed.")
        else:
            print("Process completed without deleting files.")
        sys.exit(0)  # Terminate the script execution
    # else:
    #     # Call the next function here
    #     print("Baking the output... (check the domaindots foleder)")

def secondstop():
    # List of folders to delete files from
    folders = ["input","domaindots","patterns"]

    # Prompt to ask if the process is finished
    questions = [
        {
            'type': 'confirm',
            'name': 'finished',
            'message': 'Stop the process?',
            'default': False
        }
    ]
    answers = prompt(questions)

    if answers['finished']:
        # Ask for confirmation before deleting files
        confirm_question = [
            {
                'type': 'confirm',
                'name': 'confirm_delete',
                'message': 'Are you sure you want to delete all files in the folders?',
                'default': False
            }
        ]
        confirm_answer = prompt(confirm_question)
        if confirm_answer['confirm_delete']:
            delete_files_in_folders(folders)
            print("Files deleted. Process completed.")
        else:
            print("Process completed without deleting files.")
        sys.exit(0)  # Terminate the script execution
    else:
        # Call the next function here
        print("...")

import sys
from PyInquirer import prompt, Validator, ValidationError

class FloatValidator(Validator):
    def validate(self, document):
        try:
            value = float(document.text)
            if not (0 <= value <= 1):
                raise ValidationError(
                    message='Please enter a number between 0 and 1',
                    cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(
                message='Please enter a valid number',
                cursor_position=len(document.text))

def ask_similarity_threshold():
    questions = [
        {
            'type': 'input',
            'name': 'threshold',
            'message': 'Enter the similarity threshold (between 0 and 1):',
            'validate': FloatValidator
        }
    ]
    answers = prompt(questions)
    return float(answers['threshold'])

def viz_uml_diagrams(uml_folder, plantuml_jar_path):
    # Iterate over subfolders in the uml folder
    for root, dirs, files in os.walk(uml_folder):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            # command to run for the current subfolder
            cmd = f"java -jar {plantuml_jar_path} {subfolder_path}"
            # run the command and wait for it to finish
            subprocess.run(cmd, shell=True, check=True)

def laststop():
    # List of folders to delete files from
    folders = ["input","domaindots","patterns","domain_patterns"]

    # Prompt to ask if the user wants to delete all files
    questions = [
        {
            'type': 'confirm',
            'name': 'delete_files',
            'message': 'Do you want to delete all files?',
            'default': False
        }
    ]
    answers = prompt(questions)

    if answers['delete_files']:
        delete_files_in_folders(folders)
        print("Files deleted. Process completed.")
        sys.exit(0)  # Terminate the script execution
    else:
        # Call the next function here
        print("Bye!")
        sys.exit(0)  


def process_pattern(pattern_graphs, host_graphs, converted_patterns_filtered):
    stored_integers = set()

    while True:
        # Ask the user for an input integer
        questions = [
            {
                'type': 'input',
                'name': 'patterns',
                'message': 'Enter a pattern index:',
                'validate': lambda val: val.isdigit() or 'Please enter a valid pattern'
            }
        ]
        answers = prompt(questions)

        integer = int(answers['patterns'])
        
        # Check if the integer was already given as input
        if integer in stored_integers:
            print("This patterns has already been entered. Please enter a different pattern.")
            continue

        # Store the integer
        stored_integers.add(integer)
        # Print the integer
        print(f"Stored pattern: {integer}")
        input = [str(integer)]
        selected_pattern = utils.patterns.select_sublists(pattern_graphs,input)
        #print(selected_pattern)
        find_patterns = utils.patterns.count_subgraph_isomorphisms(selected_pattern,host_graphs)
        find_patterns_clean_ = utils.patterns.remove_duplicate_graphs(find_patterns)
        node_labels = ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                    "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                    "creation", "historicalDependence", "manifestation", "participation",
                    "participational", "termination", "triggers", "instantiation", "relation"] 
        edge_labels = ["target", "specific", "general","source"]
        #find_patterns_clean = process_genset_cardinalities(find_patterns_clean_)
        converted_domain_patterns = utils.back2UML.convert_graphs_new(find_patterns_clean_)
        converted_domain_patterns_filtered = utils.generateinput.process_graphs__(node_labels, edge_labels, converted_domain_patterns)
        converted_domain_patterns_filtered_0 = utils.patterns.check_and_clean_graphs(converted_patterns_filtered, converted_domain_patterns_filtered)
        utils.UMLviz.convert_to_plantuml_domain(converted_domain_patterns_filtered_0)
        domain_patterns_folder = "./domain_patterns"
        plantuml_jar_path = "utils/plantumlGenerator.jar"
        viz_uml_diagrams(domain_patterns_folder, plantuml_jar_path)
        # Ask if the user wants to continue
        questions = [
            {
                'type': 'confirm',
                'name': 'continue',
                'message': 'Do you want to continue?',
                'default': False
            }
        ]
        answers = prompt(questions)

        if not answers['continue']:
            laststop()