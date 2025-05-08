import pandas as pd
import networkx as nx

# Load edge data
print("Loading edge data...")
edges_df = pd.read_csv("edge_table.csv")
print(f"Loaded {len(edges_df)} edges from CSV")
print("First few rows of edge data:")
print(edges_df.head())

# Create NetworkX graph
print("\nCreating NetworkX graph...")
G = nx.from_pandas_edgelist(edges_df, source='this_gene', target='other_gene', edge_attr=['weight'])
print(f"Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Calculate degrees - testing different approaches
print("\nCalculating degrees...")

# Method 1: Standard NetworkX degree method
degrees1 = dict(G.degree())
print("Method 1 - First 5 degrees:")
first_five_nodes = list(G.nodes())[:5]
for node in first_five_nodes:
    print(f"Node {node}: Degree = {degrees1[node]}")

# Method 2: Explicitly count neighbors
print("\nMethod 2 - First 5 degrees (counting neighbors):")
for node in first_five_nodes:
    neighbors = list(G.neighbors(node))
    print(f"Node {node}: Degree = {len(neighbors)}, Neighbors: {neighbors[:3]}...")

# Check for non-zero degrees
print("\nDegree statistics:")
non_zero_degrees = [d for n, d in degrees1.items() if d > 0]
print(f"Nodes with degree > 0: {len(non_zero_degrees)} out of {len(degrees1)}")
print(f"Max degree: {max(degrees1.values()) if degrees1 else 0}")
print(f"Average degree: {sum(degrees1.values())/len(degrees1) if degrees1 else 0}")

# Find top 5 nodes by degree
print("\nTop 5 nodes by degree:")
sorted_nodes = sorted(degrees1.items(), key=lambda x: x[1], reverse=True)
for node, degree in sorted_nodes[:5]:
    print(f"Node {node}: Degree = {degree}")

print("\nDone!")