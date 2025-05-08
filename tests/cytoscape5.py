import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_gene_network(edge_file, min_weight=1):
    """Create a gene network from an edge file"""
    # Read the edge data
    edges = []
    
    with open(edge_file, 'r') as f:
        # Skip header
        f.readline()
        
        for line in f:
            gene1, gene2, weight = line.strip().split(',')
            weight = int(weight)
            
            if weight >= min_weight:
                edges.append((gene1, gene2, weight))
    
    # Create network
    G = nx.Graph()
    
    # Add weighted edges
    for gene1, gene2, weight in edges:
        G.add_edge(gene1, gene2, weight=weight)
    
    print(f"Created network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def filter_network(G, method='weight', value=2):
    """Filter network using different methods"""
    filtered_G = nx.Graph()
    
    if method == 'weight':
        # Keep edges with weight >= value
        for u, v, data in G.edges(data=True):
            if data['weight'] >= value:
                filtered_G.add_edge(u, v, weight=data['weight'])
    
    elif method == 'component_size':
        # Keep components with size >= value
        for component in nx.connected_components(G):
            if len(component) >= value:
                subgraph = G.subgraph(component)
                filtered_G.add_edges_from(subgraph.edges(data=True))
    
    elif method == 'hubs':
        # Keep top 'value' hubs and their connections
        degrees = dict(G.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        top_hubs = [node for node, _ in sorted_nodes[:value]]
        
        for hub in top_hubs:
            filtered_G.add_node(hub)
            for neighbor in G.neighbors(hub):
                filtered_G.add_edge(hub, neighbor, weight=G[hub][neighbor]['weight'])
    
    elif method == 'seed':
        # Keep nodes within 'value' steps of seed node
        seed = value  # In this case, 'value' is the seed gene ID
        if seed not in G:
            return filtered_G
            
        nodes = {seed}
        current_nodes = {seed}
        
        # Expand to neighbors up to 2 steps away
        for _ in range(2):
            next_nodes = set()
            for node in current_nodes:
                next_nodes.update(G.neighbors(node))
            
            # Add new nodes
            next_nodes = next_nodes - nodes
            nodes.update(next_nodes)
            current_nodes = next_nodes
        
        filtered_G = G.subgraph(nodes).copy()
    
    print(f"Filtered network has {filtered_G.number_of_nodes()} nodes and {filtered_G.number_of_edges()} edges")
    return filtered_G

def write_to_cytoscape(G, edge_file='edge_table.csv', node_file='node_table.csv'):
    """Write network to Cytoscape-compatible files"""
    # Write edge file
    with open(edge_file, 'w') as f:
        f.write("this_gene,other_gene,weight\n")
        for u, v, data in G.edges(data=True):
            f.write(f"{u},{v},{data['weight']}\n")
    
    # Write node file with degree information
    with open(node_file, 'w') as f:
        f.write("geneID,symbol,degree\n")
        for node in G.nodes():
            # Here we use the gene ID as symbol since we don't have the mapping
            # In a real application, you would look up the gene symbol
            symbol = node
            degree = G.degree(node)
            f.write(f"{node},{symbol},{degree}\n")
    
    print(f"Network files written to {edge_file} and {node_file}")

def main():
    # Create network from your edge file
    G = create_gene_network('edge_table.csv', min_weight=1)
    
    # Try different filtering methods
    
    # Method 1: Filter by edge weight (keep edges with weight >= 2)
    weight_G = filter_network(G, method='weight', value=2)
    write_to_cytoscape(weight_G, 'weight_edges.csv', 'weight_nodes.csv')
    
    # Method 2: Filter by component size (keep components with at least 5 nodes)
    component_G = filter_network(G, method='component_size', value=5)
    write_to_cytoscape(component_G, 'component_edges.csv', 'component_nodes.csv')
    
    # Method 3: Filter by hub genes (keep top 20 highest-degree genes and their connections)
    hub_G = filter_network(G, method='hubs', value=20)
    write_to_cytoscape(hub_G, 'hub_edges.csv', 'hub_nodes.csv')
    
    # Method 4: Create seed-based network (using gene '24314' as seed)
    seed_G = filter_network(G, method='seed', value='24314')
    write_to_cytoscape(seed_G, 'seed_edges.csv', 'seed_nodes.csv')

if __name__ == "__main__":
    main()