import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import test_patterns
import test_graphClustering1
import test_graphClustering0

patternspath = "./input/outputpatterns.txt"

def extract_clusters(input_list):
    # Extract the second element from each sublist
    clusters = [item[1] for item in input_list]
    return clusters

# method 0
# pattern_graphs_ = test_graphClustering0.convertPatterns(patternspath)
# patterns_features_ = test_graphClustering0.extract_features(pattern_graphs_)
# patterns_dataframe_ = test_graphClustering0.transform_graph_data(patterns_features_)
# patterns_similarity_matrix_ = test_graphClustering0.calculate_similarity(patterns_dataframe_)
# patterns_cluster_labels = test_graphClustering0.group_similar_items(patterns_similarity_matrix_,0.2)
# pattern_graphs_clustered_ = test_graphClustering0.merge_lists(patterns_cluster_labels,pattern_graphs_)
# output_ = extract_clusters(patterns_cluster_labels)
# print(output_)

# method 1
pattern_graphs = test_patterns.convertPatterns(patternspath)
list_of_vectors = test_graphClustering1.graphs2dataframes2vectors(pattern_graphs)
singledtaframe = test_graphClustering1.transform2singledataframe(list_of_vectors)
patterns_similarity_matrix = test_graphClustering1.calculate_similarity(singledtaframe)
grouped_items = test_graphClustering1.group_similar_items(patterns_similarity_matrix,0.57)
output = extract_clusters(grouped_items)
#print(output)


trend = [[0.1,0.18], [0.15,0.18], [0.2,0.18],[0.25,0.18], [0.3,0.21], [0.35,0.27], [0.4,0.27], 
         [0.45,0.31], [0.5,0.33], [0.51,0.39], [0.52,0.45], [0.53,0.45], [0.54,0.45], [0.55,0.91], [0.56,0.91], 
         [0.57,0.94],[0.58,0.94],[0.59,0.94],[0.6,0.79], [0.65,0.64], [0.7,0.61], [0.75,0.27],
        [0.8,0.09], [0.85,0.06], [0.9,0.03]]

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


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

# for i, v in enumerate(second_numbers):
#    ax.text(i, v + 0.2, str(v), ha='center')
# for i, v in enumerate(second_numbers):
#     ax.text(i, v + 1, str(v), ha='center', va='bottom', rotation=90)
for i, v in enumerate(second_numbers):
    ax.text(i, v + 0.01, str(v), ha='center', va='bottom', rotation=90, fontsize=12, color='#565656')

plt.xlabel('Clustering Threshold', fontsize=15)
plt.ylabel('Accuracy', fontsize=15)


# Customize the color of each bar based on its value
# for i in range(len(categories)):
#     plt.gca().get_children()[i].set_facecolor(color_palette[i])
 
# ax.tick_params(labelsize=16,length=0)
# plt.box(False)
# ax.yaxis.grid(linewidth=0.5,color='grey',linestyle='-.')
# ax.set_axisbelow(True)
# ax.set_xlabel('Province',weight='bold',size=1)
# ax.set_ylabel('Minimum Wage',weight='bold',size=1)
#plt.yticks(np.arange(0, 18, 4)) #yticks starts from 0 and ends at 18, step is 4
#ax.set_yticklabels([" ","$4","$8","$12","$16"],color='#565656')
#plt.xticks(rotation=90,color='#565656')
plt.savefig('test.pdf', dpi=300)
#plt.show()



# Replace these arrays with your actual data
#true_labels = np.array(['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A'])  # True labels (ground truth)
#predicted_labels = np.array(['A', 'B', 'C', 'A', 'C', 'D', 'B', 'B', 'A', 'A'])  # Predicted labels
true_labels = np.array(['cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0', 'cluster_0','cluster_1',
                        'cluster_1','cluster_1','cluster_1','cluster_1','cluster_1','cluster_1','cluster_2', 'cluster_2',
                        'cluster_3', 'cluster_3', 'cluster_3', 'cluster_4', 'cluster_4', 'cluster_4', 'cluster_4', 'cluster_4',
                        'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5', 'cluster_5',
                        'cluster_5', 'cluster_5'])  # True labels (ground truth)
print(len(true_labels))
predicted_labels = np.array(output)  # Predicted labels

# List of all possible labels
labels = np.unique(np.concatenate((true_labels, predicted_labels)))

# Calculate the confusion matrix
cm = confusion_matrix(true_labels, predicted_labels, labels=labels)

# Calculate accuracy
accuracy = np.sum(np.diag(cm)) / np.sum(cm)

# Display the confusion matrix as a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Clusters')
plt.ylabel('True Clusters')
plt.title(f'Confusion Matrix for the Best Threshold (0.57,0.58,0.59)\nAccuracy : {accuracy:.2f}')
plt.savefig('test0.pdf', dpi=300)
#plt.show()

print(f"Accuracy: {accuracy:.2f}")





