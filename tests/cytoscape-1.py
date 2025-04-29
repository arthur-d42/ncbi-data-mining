import pandas as pd
import networkx as nx
from py2cytoscape.data.cyrest_client import CyRestClient

edges_df = pd.read_csv("tests/edge_table.csv")
nodes_df = pd.read_csv("tests/node_table.csv")

# Lav NetworkX graf
G = nx.from_pandas_edgelist(edges_df, source='this_gene', target='other_gene', edge_attr=True)

# Tilføj nodedata
for _, row in nodes_df.iterrows():
    G.nodes[int(row['geneID'])]['symbol'] = row['symbol']

# Send til Cytoscape
cy = CyRestClient()
cy.network.create_from_networkx(G)
