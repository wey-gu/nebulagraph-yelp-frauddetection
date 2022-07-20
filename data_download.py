import os

import dgl
import numpy as np


OUTPUT_FOLDER = "data"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# get dataset from dgl
dataset = dgl.data.FraudDataset("yelp")
graph = dataset[0]

# get the node features, labels
nodes_feature = graph.ndata['feature'].numpy()
nodes_label = graph.ndata['label'].numpy().reshape(-1, 1)
node_records = np.append(nodes_label, nodes_feature, axis=1)
nodes_with_id = np.insert(node_records, node_records.shape[1], values=[
                          range(0, node_records.shape[0])], axis=1)

# export the node features and labels to csv
np.savetxt(f"{ OUTPUT_FOLDER }/vertices.csv", nodes_with_id,
           fmt='%f,' * nodes_feature.shape[1] + '%d,%d')

for edge_type in graph.etypes:
    # get the edge per type, there is no feature in the edge
    src_edges, dst_edges = graph.edges(etype=edge_type)
    edge_records = np.append(
        src_edges.numpy().reshape(-1, 1), dst_edges.numpy().reshape(-1, 1), axis=1)
    # export the edge features to csv
    np.savetxt(f"{ OUTPUT_FOLDER }/{ edge_type }.csv",
               edge_records, fmt='%d,%d')
