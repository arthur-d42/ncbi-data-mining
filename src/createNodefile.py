# Import libraries
import sys
import pathlib
import gzip

# Importing functions from other files
from importData import file_exists

def geneID_to_symbol_dict(tax_id, info_file):
    """Function that takes a tax_id and finds the appropriate symbol in the gene_info.gz file"""
    symbol_dict = {}
    
    try:
        # Checking whether input file exists
        if not pathlib.Path(info_file).is_file():
            raise FileNotFoundError(f"Input file '{info_file}' does not exist.")

        with gzip.open(info_file, 'rt') as file:
            for line in file:
                split_line = line.split()
                # Looks for lines with tax_id, finds the gene ID, and the symbol from that line and adds to dict
                if str(split_line[0]) == str(tax_id):
                    geneID = split_line[1]
                    symbol = split_line[2]
                    symbol_dict[geneID] = symbol
            
            return symbol_dict
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    

def create_node_file(edge_file, node_file, tax_id, info_file):
    """Function that takes an edge_file, the name of the wished output file, and creates the edges with names decided from 
    tax_id and the info file"""
    
    print("\nStarting creation of node file")
    
    # Create dict that translates geneID to symbol
    symbol_dict = geneID_to_symbol_dict(tax_id, info_file)
    
    # unique gene IDs
    unique_gene_ids = set()
    
    # Read edge file 
    try:
        with open(edge_file, 'r') as f:
            # Skip header
            next(f)
            
            for line in f:
                # Split by comma and extract gene IDs
                split_line = line.strip().split(',')
                gene1 = split_line[0]
                gene2 = split_line[1]
                    
                # Add both genes to the set
                # Will not add if not unique :)
                unique_gene_ids.add(gene1)
                unique_gene_ids.add(gene2)
        print(f"Created node file in location {node_file}")
    except Exception as e:
        print(f"Error reading edge file: {e}")
        sys.exit(1)
    
    # Write file
    try:
        with open(node_file, 'w') as f:
            # Write header
            f.write("geneID,symbol\n")
            
            # Write each unique gene ID and its symbol
            for gene_id in sorted(unique_gene_ids):
                # Look up symbol in dictionary, use empty string if not found
                symbol = symbol_dict.get(gene_id, "")
                f.write(f"{gene_id},{symbol}\n")
        
        print("Successfully created node file")
        
    except Exception as e:
        print(f"Error writing node file: {e}")
        sys.exit(1)

def main():
    """Function that runs create_node_file() while asking for input"""
    
    while True:
        try:
            tax_id_input = input("\nPlease enter a tax ID (or press Enter for 69 as default): ").strip()
            tax_id = int(tax_id_input) if tax_id_input else 69
            break
        except ValueError:
            print("Error: Tax ID must be a number. Please try again.")
    
    while True:
        edge_file = input("\nPlease enter the path to the edge file (or press Enter for default): ").strip() or 'data/edge_table.csv'
        if file_exists(edge_file):
            break
        print(f"Error: Edge file '{edge_file}' not found. Please try again.")

    while True:
        info_file = input("\nPlease enter the path to the gene info file (or press Enter for default): ").strip() or "data/downloaded/gene_info.gz"
        if file_exists(info_file):
            break
        print(f"Error: Info file '{info_file}' not found. Please try again.")

    node_file = input("\nPlease enter where you want the node file (or press Enter for default): ").strip() or 'data/node_table.csv'

    # Call create_gene_translation_file
    create_node_file(edge_file, node_file, tax_id, info_file)
    


if __name__ == "__main__":
    # For running the program in terminal
    main()
