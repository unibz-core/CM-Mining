import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import test_patterns
import test_graphClustering1

patternspath = "./input/outputpatterns.txt"

# def extract_clusters(input_list):
#     # Extract the second element from each sublist
#     clusters = [item[1] for item in input_list]
#     return clusters

def add_indices_to_list(input_list):
    result_list = []
    for index, item in enumerate(input_list):
        result_list.append([index, item])
    return result_list

def order_sublists_by_index(input_list):
    ordered_list = sorted(input_list, key=lambda x: x[0])
    return ordered_list

def extract_indexes(list_of_lists):
    indexes = [item[0] for item in list_of_lists]
    return indexes

# def extract_cluster(list_of_lists):
#     indexes = [item[1] for item in list_of_lists]
#     return indexes

ground_truth = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 'cluster_1', 'cluster_1', 
                'cluster_1', 'cluster_2', 'cluster_1', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 
                'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 
                'cluster_5', 'cluster_5', 'cluster_5']
output = ['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 
          'cluster_1', 'cluster_1', 'cluster_1', 'cluster_2', 'cluster_1', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 
          'cluster_4', 'cluster_4', 'cluster_4', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 
          'cluster_5', 'cluster_5', 'cluster_2', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5']

# # method 1
pattern_graphs = test_patterns.convertPatterns(patternspath)
list_of_vectors = test_graphClustering1.graphs2dataframes2vectors(pattern_graphs)
singledtaframe = test_graphClustering1.transform2singledataframe(list_of_vectors)
patterns_similarity_matrix = test_graphClustering1.calculate_similarity(singledtaframe)
grouped_items = test_graphClustering1.group_similar_items(patterns_similarity_matrix,0.6) 
# output_ = extract_clusters(grouped_items)
# #print(output_)

ordered_grouped_items = order_sublists_by_index(grouped_items)
# cluster_ordered = extract_cluster(ordered_grouped_items)
# print(cluster_ordered)
result = add_indices_to_list(ground_truth)
indexes = extract_indexes(result)

# ### Confusion matrix
# Replace these arrays with your actual data
true_labels = np.array(['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_1', 'cluster_1', 'cluster_1', 'cluster_1', 
                'cluster_1', 'cluster_2', 'cluster_1', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 
                'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 
                'cluster_5', 'cluster_5', 'cluster_5']
)  # True labels (ground truth)

predicted_labels = np.array(output)  # Predicted labels

# # List of all possible labels
labels = np.unique(np.concatenate((true_labels, predicted_labels)))

# Calculate the confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=labels)

# Calculate accuracy
accuracy = np.sum(np.diag(cm)) / np.sum(cm)

correct_mask = np.eye(len(labels), dtype=bool)
incorrect_mask = ~correct_mask

# Display the confusion matrix as a heatmap
plt.figure(figsize=(8, 6))
#sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    mask=incorrect_mask,  # Masking incorrect predictions
    xticklabels=labels,
    yticklabels=labels,
    cbar_kws={'format': ''}, 
    cbar=True,
    vmin=0,  # Set the minimum value of the color scale
    vmax=3,
)
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Reds",  # Color for correct predictions
    mask=correct_mask,  # Masking correct predictions
    xticklabels=labels,
    yticklabels=labels,
    cbar=False,
    vmin=0,  # Set the minimum value of the color scale
    vmax=15,
)

plt.xlabel('Predicted Clusters')
plt.ylabel('True Clusters')
plt.title(f'Confusion Matrix for the Best Threshold (0.60,0.61)\nAccuracy : 0.93') #{accuracy:.2f}'
plt.savefig('test0.pdf', dpi=300)
plt.show()
# print(f"Accuracy: {accuracy:.2f}")

### Accuracy calculation, for each trial

from itertools import product
def solve(l1, l2):
   return list(product(l1, l2))

def calculate_accuracy(A, B, P):
    accuracy = 0
    numPairs = 0
    for i in P:
        for j in P:
            # Check if the 'cluster' values are equal for A and B
            checkPredicted = A[i][1] == A[j][1]
            checkReal = B[i][1] == B[j][1]
            
            if checkPredicted == checkReal:
                accuracy += 1
            numPairs += 1

    if numPairs == 0:
        return 0.0
    else:
        accuracy = accuracy / numPairs
        return accuracy

final_result = calculate_accuracy(ordered_grouped_items, result, indexes)
print("Accuracy:", final_result)

### Accuracy plot
trend = [[0.1,0.24], [0.15,0.29], [0.2,0.44],[0.25,0.65], [0.3,0.76], [0.35,0.74], [0.4,0.70], 
         [0.45,0.72], [0.5,0.76], [0.51,0.85], [0.52,0.90], [0.53,0.90], [0.54,0.90], [0.55,0.91], [0.56,0.91], 
         [0.57,0.92],[0.58,0.92],[0.59,0.92],[0.6,0.93],[0.61,0.93],[0.62,0.87],[0.63,0.88],[0.65,0.88],[0.64,0.88],[0.7,0.83],[0.75,0.74],
        [0.8,0.72], [0.85,0.72], [0.9,0.71], [0.95,0.69], [0.99,0.69]]

first_numbers = [item[0] for item in trend]
second_numbers = [item[1] for item in trend]
#sns.set(style="whitegrid", color_codes=True)
colormap = plt.cm.Blues
plt.figure(figsize=(8, 7))
ax = sns.barplot(x=first_numbers,y=second_numbers, hue=first_numbers, palette=colormap(second_numbers), legend=False, alpha=1)
plt.xticks(rotation=90,color='#565656')
plt.xticks(fontsize=12)
ax.set_ylim(0, 1.05)
ax.set_yticklabels([])
for i, v in enumerate(second_numbers):
    ax.text(i, v + 0.01, str(v), ha='center', va='bottom', rotation=90, fontsize=12, color='#565656')

plt.xlabel('Clustering Threshold', fontsize=15)
plt.ylabel('Accuracy', fontsize=15)
plt.savefig('test.pdf', dpi=300)
plt.show()

######

