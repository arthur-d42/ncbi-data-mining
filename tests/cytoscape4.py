import pandas as pd
import networkx as nx
import os
import json

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
        nodes_df = pd.DataFrame({'geneID': list(G.nodes())})
        
    return G, nodes_df

def analyze_and_filter(G, filter_method="top_n", filter_value=10):
    """Analyze network and filter based on criteria"""
    # Calculate node degrees
    degrees = dict(G.degree())
    
    # Filter graph
    if filter_method == "top_n":
        # Get top N hubs
        top_hubs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:filter_value]
        top_hub_ids = [node for node, _ in top_hubs]
        
        # Create subgraph with hubs and their neighbors
        filtered_G = nx.Graph()
        for hub in top_hub_ids:
            filtered_G.add_node(hub)
            for neighbor in G.neighbors(hub):
                filtered_G.add_edge(hub, neighbor, weight=G[hub][neighbor].get('weight', 1))
    else:
        # Filter by minimum degree
        min_degree = filter_value
        nodes_to_keep = [node for node, degree in degrees.items() if degree >= min_degree]
        filtered_G = G.subgraph(nodes_to_keep).copy()
    
    # Add degree attribute to nodes
    for node in filtered_G.nodes():
        filtered_G.nodes[node]['degree'] = degrees[node]
    
    return filtered_G, degrees

def export_for_cytoscape(G, prefix="gene_network"):
    """Export graph for Cytoscape"""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Export as GraphML (Cytoscape can import this)
    nx.write_graphml(G, f"output/{prefix}.graphml")
    print(f"Network exported as GraphML: output/{prefix}.graphml")
    
    # Create proper Cytoscape.js JSON manually
    cyto_json = {
        'data': {},
        'directed': G.is_directed(),
        'multigraph': G.is_multigraph(),
        'elements': {
            'nodes': [],
            'edges': []
        }
    }
    
    # Add nodes with proper string IDs
    for node, attrs in G.nodes(data=True):
        node_str = str(node)  # Ensure node ID is a string
        node_data = {'id': node_str}
        
        # Copy all attributes
        for k, v in attrs.items():
            node_data[k] = v
            
        # Add name if not present
        if 'name' not in node_data:
            if 'symbol' in node_data:
                node_data['name'] = node_data['symbol']
            else:
                node_data['name'] = node_str
                
        cyto_json['elements']['nodes'].append({'data': node_data})
    
    # Add edges with proper string IDs for source and target
    for source, target, attrs in G.edges(data=True):
        edge_data = {
            'source': str(source),  # Ensure source ID is a string
            'target': str(target),  # Ensure target ID is a string
        }
        
        # Copy all edge attributes
        for k, v in attrs.items():
            edge_data[k] = v
            
        cyto_json['elements']['edges'].append({'data': edge_data})
    
    # Write to file
    with open(f"output/{prefix}.json", 'w') as f:
        json.dump(cyto_json, f, indent=2)
    print(f"Network exported as Cytoscape JSON: output/{prefix}.json")
    
    # Export CSV tables
    node_data = []
    for node, attrs in G.nodes(data=True):
        node_info = {'id': node}
        node_info.update(attrs)
        node_data.append(node_info)
    
    nodes_df = pd.DataFrame(node_data)
    nodes_df.to_csv(f"output/{prefix}_nodes.csv", index=False)
    print(f"Node table exported: output/{prefix}_nodes.csv")
    
    edge_data = []
    for source, target, attrs in G.edges(data=True):
        edge_info = {
            'source': source,
            'target': target
        }
        edge_info.update(attrs)
        edge_data.append(edge_info)
    
    edges_df = pd.DataFrame(edge_data)
    edges_df.to_csv(f"output/{prefix}_edges.csv", index=False)
    print(f"Edge table exported: output/{prefix}_edges.csv")
    
    return f"output/{prefix}.json"

def main():
    # Get file inputs
    edge_file = input("Edge table file (default: edge_table.csv): ") or "edge_table.csv"
    node_file = input("Node table file (default: node_table.csv): ") or "node_table.csv"
    
    # Load network
    G, _ = load_data(edge_file, node_file)
    print(f"Loaded network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    # Choose filtering method
    filter_choice = input("Filter by: (1) Top N hubs or (2) Minimum degree [default: 1]: ") or "1"
    
    if filter_choice == "1":
        n = int(input("Number of top hubs [default: 10]: ") or "10")
        filtered_G, degrees = analyze_and_filter(G, "top_n", n)
        prefix = f"gene_network_top{n}"
    else:
        threshold = int(input("Minimum degree [default: 3]: ") or "3")
        filtered_G, degrees = analyze_and_filter(G, "min_degree", threshold)
        prefix = f"gene_network_min{threshold}"
    
    # Display top genes
    top_genes = sorted(dict(filtered_G.degree()).items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop genes in filtered network:")
    for gene, degree in top_genes:
        symbol = filtered_G.nodes[gene].get('symbol', 'Unknown')
        print(f"Gene {gene} (Symbol: {symbol}): {degree} connections")
    
    # Export for Cytoscape
    output_file = export_for_cytoscape(filtered_G, prefix)
    print(f"\nFiltered network: {filtered_G.number_of_nodes()} nodes, {filtered_G.number_of_edges()} edges")
    print(f"Network exported for Cytoscape: {output_file}")
    print("\nTo import in Cytoscape:")
    print("1. Open Cytoscape")
    print("2. Go to File → Import → Network → From File...")
    print(f"3. Select the {output_file} file")
    print("4. In the import dialog, make sure to select 'source' and 'target' columns correctly")

if __name__ == "__main__":
    main()