import pandas as pd
import networkx as nx
import os
import py4cytoscape as p4c

def load_data(edge_file, node_file=None):
    """Load data from CSV files into NetworkX graph with edge_weights"""
    edges_df = pd.read_csv(edge_file)
    
    # Create a NetworkX graph with edge weights
    G = nx.from_pandas_edgelist(edges_df, source='this_gene', target='other_gene', edge_attr=['weight'])
    
    # Load node data if available
    if node_file and os.path.exists(node_file):
        nodes_df = pd.read_csv(node_file)
        # Add node attributes
        for _, row in nodes_df.iterrows():
            node_id = row['geneID']
            if node_id in G.nodes:
                # Convert node_id to string if it's not already
                G.nodes[node_id]['symbol'] = row['symbol']
    
    else:
        # Create node table with just IDs and prints that no symbols are found
        print('Symbol not found. Note table with IDs have been created')
    
    return G, nodes_df

def analyze_and_filter(G, n, m):
    """Analyze network and filter based on criteria"""
    # Calculate node degrees
    degrees = dict(G.degree())
    
    print(G)
    
    # Find noder med grad mindre end m
    nodes_to_remove = [node for node, degree in degrees.items() if degree < m]
    
    # Fjern disse noder fra grafen
    G.remove_nodes_from(nodes_to_remove)
    
    print(G)
    
    
    # Get top N hubs
    top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:n]
    top_hub_ids = [node for node, _ in top_hubs]
    
    return top_hub_ids, degrees


def main():
    # Get file inputs
    print("\nRemember to have Cytoscape from Unix system")
    print("\nYou might need a version of X running")
    
    n = int(input("\nNumber of top hubs (or press Enter for 10 as default): ") or "10")
    
    m = int(input("\nNumber of top hubs (or press Enter for 2 as default): ") or "2")
    
    edge_file = input("\nEnter path to edge_table.csv (or press Enter for default): ").strip() or 'data/edge_table.csv'

    node_file = input("Enter path to node_table.csv (or press Enter for default): ").strip() or 'data/node_table.csv'
    
    # Load network
    G, _ = load_data(edge_file, node_file)
    print(f"\nLoaded network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Filter
    top_genes, degrees = analyze_and_filter(G, n, m)
    
    # Display top genes
    print("\nTop genes in network:")
    for gene in top_genes:
        # Unknown as default value if no symbol
        symbol = G.nodes[gene].get('symbol', 'Unknown')
        print(f"Gene {gene} (Symbol: {symbol}): {degrees[gene]} connections")
    
    
    # Create network in Cytoscape using py4cytoscape
    network_name = "Gene Network"
    network_suid = p4c.create_network_from_networkx(G, network_name)

    # Set node label to symbol
    p4c.set_node_label_mapping('symbol', network=network_suid)

    # Map discrete values for edge line width
    p4c.set_edge_line_width_mapping(**p4c.gen_edge_width_map('weight', mapping_type='d'))
    
    print(f"Created network with SUID: {network_suid}")



if __name__ == "__main__":
    # For running the program in terminal
    main()