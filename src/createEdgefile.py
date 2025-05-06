# Import libraries
import subprocess
import sys

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
    with open(edge_file, 'w') as out:
        # Write header
        out.write("this_gene,other_gene,weight\n")
        
        # Write each entry
        for (gene1, gene2), weight in gene_dict.items():
            if weight >= weight_min:
                out.write(f"{gene1},{gene2},{weight}\n")
    return



def create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min):
    """Function that runs above functions while asking for input"""
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




if __name__ == "__main__":
    try:
        # Defaults for file paths
        tmp_file = "data/tmp_file"
        sorted_tmp_file = "data/sorted_tmp_file"
        edge_file = 'data/edge_table.csv'
        
        # Ask for min weight
        weight_min = int(input("Please write a minimum weight (suggestion is 1): "))
        create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min)
    
    except ValueError: 
        print("Error: weight_min must be a number")
        sys.exit(1)
    
