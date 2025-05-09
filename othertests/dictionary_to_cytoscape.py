import pandas as pd
import networkx as nx
import py4cytoscape as p4c

# Load data
edges_df = pd.read_csv("data/edge_table.csv")
nodes_df = pd.read_csv("data/node_table.csv")

# Create NetworkX graph with edge weights
G = nx.from_pandas_edgelist(edges_df, source='this_gene', target='other_gene', edge_attr=['weight'])

# Add node data
for _, row in nodes_df.iterrows():
    node_id = row['geneID']
    if node_id in G.nodes:
        G.nodes[node_id]['symbol'] = row['symbol']

# Create network in Cytoscape using py4cytoscape
network_name = "Gene Network"
network_suid = p4c.create_network_from_networkx(G, network_name)

# Set node label to symbol
p4c.set_node_label_mapping('symbol', network=network_suid)


p4c.set_edge_line_width_mapping(**p4c.gen_edge_width_map('weight', mapping_type='d'))

print(f"Created network with SUID: {network_suid}")
