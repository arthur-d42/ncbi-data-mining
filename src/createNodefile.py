# Import libraries
import sys
import pathlib
import gzip

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
                if split_line[0] == tax_id:
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
                
    except Exception as e:
        print(f"Error writing node file: {e}")
        sys.exit(1)

def main():
    """Function that runs create_node_file() while asking for input"""
    try:
        # Ask for tax_id
        tax_id = input("Please write a tax_id: ")
        if not tax_id.isdigit():
            print(f"Error: tax_id must be a number. You entered: '{tax_id}'")
            sys.exit(1)

        # Ask user for file paths or use defaults
        edge_file = input("Enter path to edge_table.csv (or press Enter for default): ").strip() or 'data/edge_table.csv'

        node_file = input("Enter path to node_table.csv (or press Enter for default): ").strip() or 'data/node_table.csv'

        info_file = input("Enter path to gene_info.gz (or press Enter for default): ").strip() or "data/downloaded/gene_info.gz"

        # Call create_gene_translation_file
        create_node_file(edge_file, node_file, tax_id, info_file)
        print(f"Created node file in location {node_file}")
    except:
        print("Error") 
        sys.exit(1)


if __name__ == "__main__":
    # For running the program in terminal
    main()
