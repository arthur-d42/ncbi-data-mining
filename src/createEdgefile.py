# Import libraries
import subprocess
import sys

# Importing functions from other files
from importData import file_exists

def sort_file(file, sorted_file):
    """Function that sorts files based on 3 column, and hereafter by 2 column.
    It is sorted as a number, which leaves header at the top and a more logical flow so that 124 will be higher than 13"""
    subprocess.run(["sort", "-k3,3n", "-k2,2n", file, "-o", sorted_file], check=True)
    return


def put_in_dict(sorted_file):
    """Converts a sorted tmp_file to a dictionary of gene pair interactions with counts."""
    
    # Create initial variables
    interaction_dict = {}
    current_genes = []
    current_pubmed_id = 0
    
    try:
        # Open file for reading
        with open(sorted_file, 'r') as file:
            
            # Read header line and skip
            file.readline()
            for line in file:
                split_line = line.strip().split()
                
                pubmed_id = split_line[2]
                gene = split_line[1]
                
                #first id
                if current_pubmed_id == 0:
                    current_pubmed_id = pubmed_id

                if pubmed_id == current_pubmed_id:
                    current_genes.append(gene)
                    
                else:
                    # No need for this when sorting in bash
                    # current_genes.sort()
                    if 2 <= len(current_genes) < 1000:
                        for i in range(len(current_genes)):
                            this_gene = current_genes[i]
                            for other_gene in current_genes[i+1:]:
                                edge = (this_gene, other_gene)
                                
                                if edge not in interaction_dict:
                                    interaction_dict[edge] = 1
                                else: 
                                    interaction_dict[edge] += 1    
                    current_pubmed_id = pubmed_id
                    current_genes = [gene]
        
        # Process the last group of genes (final pubmed_id block)
        if 2 <= len(current_genes) < 1000:
            for i in range(len(current_genes)):
                this_gene = current_genes[i]
                for other_gene in current_genes[i+1:]:
                    edge = (this_gene, other_gene)
                    
                    if edge not in interaction_dict:
                        interaction_dict[edge] = 1
                    else: 
                        interaction_dict[edge] += 1    
        return interaction_dict

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def write_dict_to_csv(gene_dict, edge_file, weight_min):
    """Function that writes edge_file to to from a dict with edges and a weight. Selects only edges with a minimum of weight"""
    try:
        with open(edge_file, 'w') as out:
            # Write header
            out.write("this_gene,other_gene,weight\n")
            
            # Write each entry
            for (gene1, gene2), weight in gene_dict.items():
                if weight >= weight_min:
                    out.write(f"{gene1},{gene2},{weight}\n")
        print(f"Successfully created edge file in location {edge_file}")
    except Exception as e:
        print(f"Error while writing to file '{edge_file}': {e}")
        sys.exit(1)


def create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min):
    """Function that creates an edge file (csv) from a tmp file, creating a sorted tmp file with a minimum weight"""
    print("\nStarting creation of edge file")
    
    # Sort tmp_file
    sort_file(tmp_file, sorted_tmp_file)
    
    # Make edge_dict from sorted_tmp_file
    edge_dict = put_in_dict(sorted_tmp_file)
    edge_dict = {k: v for k, v in sorted(edge_dict.items(), key=lambda item: item[1])}
    
    try:
        write_dict_to_csv(edge_dict, edge_file, weight_min)
    
    except:
        print(f"An error occured while writing edge file to {edge_file}")
        sys.exit(1)


def main():
    """Function that runs create_node_file() while asking for input"""
    while True:
        try:
            weight_min_input = input("\nPlease enter the minimum weight of the edges you want (or press Enter for 3 as default): ").strip()
            weight_min = int(weight_min_input) if weight_min_input else 3
            break
        except ValueError: 
            print("Error: weight_min must be a number. Please try again.")
        
        
    while True:
        tmp_file = input("\nPlease enter the path to the temporary file (or press Enter for default): ").strip() or "data/tmp_file.tsv"
        if file_exists(tmp_file):
            break
        print(f"Error: Temporary file '{tmp_file}' not found. Please try again.")

    sorted_tmp_file = input("\nPlease enter where you want the sorted temporary file (or press Enter for default): ").strip() or "data/sorted_tmp_file.tsv"

    edge_file = input("\nPlease enter where you want the edge file (or press Enter for default): ").strip() or 'data/edge_table.csv'

    create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min)   

if __name__ == "__main__":
    # For running the program in terminal
    main()
