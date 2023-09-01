import os
import random
import shutil

import os
import random
import shutil

def extract_files_randomly(input_folder, output_folder, n_partitions, n_files_per_partition):
    # Get a list of all files in the input folder
    all_files = os.listdir(input_folder)
    
    # Shuffle the list of files
    random.shuffle(all_files)
    
    # Calculate the total number of files to select
    total_files_to_select = n_partitions * n_files_per_partition
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Randomly select files and copy them to the output folder
    for i in range(0, total_files_to_select, n_files_per_partition):
        selected_files = all_files[i:i + n_files_per_partition]
        for file_name in selected_files:
            source_path = os.path.join(input_folder, file_name)
            destination_path = os.path.join(output_folder, file_name)
            shutil.copy(source_path, destination_path)
    
    print(f"Randomly extracted {total_files_to_select} files and saved to {output_folder}")

# Example usage
input_folder = "input_folder"
output_folder = "output_folder"
n_partitions = 4
n_files_per_partition = 2

extract_files_randomly(input_folder, output_folder, n_partitions, n_files_per_partition)

