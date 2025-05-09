import pandas as pd
import networkx as nx
import os
import json
import py4cytoscape as p4c

def load_data(edge_file, node_file=None):
    """Load data from CSV files"""
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
        # Create node table with just IDs
        print('Symbol not found')
    return G, nodes_df

def analyze_and_filter(G, filter_value=10):
    """Analyze network and filter based on criteria"""
    # Calculate node degrees
    degrees = dict(G.degree())
    
    # Filter graph
    # Get top N hubs
    top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:filter_value]
    top_hub_ids = [node for node, _ in top_hubs]
    
    return top_hub_ids, degrees


def main():
    # Get file inputs
    edge_file = input("Edge table file (default: edge_table.csv): ") or "data/edge_table.csv"
    node_file = input("Node table file (default: node_table.csv): ") or "data/node_table.csv"
    
    # Load network
    G, _ = load_data(edge_file, node_file)
    print(f"Loaded network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Choose filtering method


    n = int(input("Number of top hubs [default: 10]: ") or "10")
    top_genes, degrees = analyze_and_filter(G, n)
    print(top_genes)
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

    # REMEMBER TO HAVE CYTOSCAPE OPEN
    print(f"Created network with SUID: {network_suid}")
    # Export for Cytoscape
    # Add this
    output_file = "Output file"
    # output_file = export_for_cytoscape(G)
    # print(f"Network exported for Cytoscape: {output_file}")
    # print("\nTo import in Cytoscape:")
    # print("1. Open Cytoscape")
    # print("2. Go to File → Import → Network → From File...")
    # print(f"3. Select the file")
    # print("4. In the import dialog, make sure to select 'source' and 'target' columns correctly")

if __name__ == "__main__":
    main()