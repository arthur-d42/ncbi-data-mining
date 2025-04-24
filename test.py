import pandas as pd
import numpy as np
from itertools import combinations
import time
import os

def process_gene_network(input_file, output_file, chunksize=100000):
    """
    Process gene-pubmed relationships and create a network of gene interactions
    using pandas for efficient data handling.
    
    Args:
        input_file: Path to the input file (tab-separated, columns: tax_id, GeneID, PubMed_ID)
        output_file: Path to save the output file (gene1, gene2, weight)
        chunksize: Number of rows to process at once
    """
    start_time = total_time = time.time()
    print(f"Starting processing of {input_file}")
    
    # Create an empty DataFrame to store the results
    edges_df = pd.DataFrame(columns=['gene1', 'gene2', 'weight'])
    
    # Process the file in chunks to handle large files
    for chunk_idx, chunk in enumerate(pd.read_csv(input_file, sep='\t', comment='#', 
                                                 names=['tax_id', 'GeneID', 'PubMed_ID'],
                                                 chunksize=chunksize)):
        chunk_time = time.time()
        print(f"Processing chunk {chunk_idx+1} ({len(chunk)} rows)...")
        
        # Group by PubMed_ID to get all genes mentioned in each paper
        grouped = chunk.groupby('PubMed_ID')['GeneID'].apply(list).reset_index()
        
        # Generate all gene pairs from each paper
        chunk_edges = []
        for _, row in grouped.iterrows():
            genes = sorted(row['GeneID'])  # Sort to ensure consistent ordering
            if len(genes) > 1:
                # Generate all unique pairs
                for gene1, gene2 in combinations(genes, 2):
                    # Ensure gene1 <= gene2 for consistency
                    if gene1 > gene2:
                        gene1, gene2 = gene2, gene1
                    chunk_edges.append((gene1, gene2))
        
        # Count occurrences of each edge in this chunk
        if chunk_edges:
            temp_df = pd.DataFrame(chunk_edges, columns=['gene1', 'gene2'])
            temp_counts = temp_df.groupby(['gene1', 'gene2']).size().reset_index(name='weight')
            
            # Merge with existing results
            if edges_df.empty:
                edges_df = temp_counts
            else:
                # Combine with existing edges, adding weights
                edges_df = pd.concat([edges_df, temp_counts])
                edges_df = edges_df.groupby(['gene1', 'gene2'])['weight'].sum().reset_index()
        
        print(f"Chunk {chunk_idx+1} processed in {time.time() - chunk_time:.2f} seconds")
        print(f"Current network has {len(edges_df)} edges")
    
    # Sort by weight (most strongly connected pairs first)
    edges_df = edges_df.sort_values('weight', ascending=False)
    
    # Save to file
    edges_df.to_csv(output_file, sep='\t', index=False)
    
    print(f"Processing completed in {time.time() - start_time:.2f} seconds")
    print(f"Network with {len(edges_df)} edges saved to {output_file}")
    return edges_df

def filter_network_for_cytoscape(network_file, output_file, min_weight=2, max_edges=None):
    """
    Filter the network to a manageable size for visualization in Cytoscape.
    
    Args:
        network_file: Path to the full network file
        output_file: Path to save the filtered network
        min_weight: Minimum edge weight to include
        max_edges: Maximum number of edges to include (takes highest weights first)
    """
    # Load the network
    df = pd.read_csv(network_file, sep='\t')
    
    # Filter by minimum weight
    filtered = df[df['weight'] >= min_weight]
    
    # Take top edges if specified
    if max_edges is not None and len(filtered) > max_edges:
        filtered = filtered.nlargest(max_edges, 'weight')
    
    # Save to file
    filtered.to_csv(output_file, sep='\t', index=False)
    print(f"Filtered network with {len(filtered)} edges saved to {output_file}")
    
    # Generate basic network statistics
    print(f"Network statistics:")
    print(f"- Total edges: {len(filtered)}")
    print(f"- Unique genes: {len(set(filtered['gene1']).union(set(filtered['gene2'])))}")
    print(f"- Weight range: {filtered['weight'].min()} to {filtered['weight'].max()}")
    print(f"- Average weight: {filtered['weight'].mean():.2f}")
    
    return filtered

def export_to_cytoscape(network_file, output_file=None, include_gene_info=False, gene_info_file=None):
    """
    Export the network to Cytoscape-compatible formats.
    
    Args:
        network_file: Path to the network file
        output_file: Path to save the Cytoscape file (default is network_file with _cytoscape suffix)
        include_gene_info: Whether to include gene info from NCBI gene_info file
        gene_info_file: Path to gene_info file if include_gene_info is True
    """
    if output_file is None:
        base, ext = os.path.splitext(network_file)
        output_file = f"{base}_cytoscape{ext}"
    
    # Load the network
    network = pd.read_csv(network_file, sep='\t')
    
    # If including gene info
    if include_gene_info and gene_info_file:
        # Load gene info (only necessary columns)
        gene_info = pd.read_csv(gene_info_file, sep='\t', comment='#', 
                                usecols=['GeneID', 'Symbol', 'description'])
        
        # Create node attribute file
        unique_genes = set(network['gene1']).union(set(network['gene2']))
        nodes = pd.DataFrame({'GeneID': list(unique_genes)})
        
        # Merge with gene info
        nodes = nodes.merge(gene_info, on='GeneID', how='left')
        
        # Save node attributes
        node_file = f"{os.path.splitext(output_file)[0]}_nodes.tsv"
        nodes.to_csv(node_file, sep='\t', index=False)
        print(f"Node attributes saved to {node_file}")
    
    # Save edge file in Cytoscape format
    network.to_csv(output_file, sep='\t', index=False)
    print(f"Edge list saved to {output_file}")

if __name__ == "__main__":
    # Example usage
    input_file = "data/sorted_tmpfile"
    output_file = "data/gene_network.tsv"
    
    # Process the full network
    process_gene_network(input_file, output_file)
    
    # Filter for visualization
    filtered_file = "data/gene_network_filtered.tsv"
    filter_network_for_cytoscape(output_file, filtered_file, min_weight=2, max_edges=1000)
    
    # Export to Cytoscape (optionally with gene info)
    # If you have the gene_info file:
    # export_to_cytoscape(filtered_file, include_gene_info=True, gene_info_file="data/gene_info")
    # Or without gene info:
    export_to_cytoscape(filtered_file)
