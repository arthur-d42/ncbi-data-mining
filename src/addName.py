# Import libraries
import sys
import pathlib
import gzip

def geneID_to_symbol_dict(taxID, filepath):
    filepath = "data/downloaded/gene_info.gz"
    
    symbol_dict = {}
    
    try:
        # Checking whether input file exists
        if not pathlib.Path(filepath).is_file():
            raise FileNotFoundError(f"Input file '{filepath}' does not exist.")

        with gzip.open(filepath, 'rt') as file:
            for line in file:
                split_line = line.split()
                if split_line[0] == taxID:
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
    

def create_gene_translation_file(input_file, output_file, symbol_dict):
    # unique gene IDs. Set because unique
    unique_gene_ids = set()
    
    # Read input file 
    with open(input_file, 'r') as f:
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
    
    # Write file
    with open(output_file, 'w') as f:
        # Write header
        f.write("geneID,symbol\n")
        
        # Write each unique gene ID and its symbol
        for gene_id in sorted(unique_gene_ids):
            # Look up symbol in dictionary, use empty string if not found
            symbol = symbol_dict.get(gene_id, "")
            f.write(f"{gene_id},{symbol}\n")


if __name__ == "__main__":
    filepath = "data/downloaded/gene_info.gz"
    symbol_dict = geneID_to_symbol_dict(sys.argv[1], filepath)
    create_gene_translation_file('edge_table.csv', 'node_table.csv', symbol_dict)

