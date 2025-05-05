# Import libraries
import subprocess
import sys

def sort_file(input_file, output_file):
    """Function that sorts files based on 3 column, and hereafter by 2 column.
    It is sorted as a number, which leaves header at the top and a more logical flow so that 124 will be higher than 13"""
    subprocess.run(["sort", "-k3,3n", "-k2,2n", input_file, "-o", output_file])
    return


def put_in_dict(file):
    """Function that takes a file in the format of """
    
    # Create initial variables
    interaction_dict = {}
    current_genes = []
    current_pubmed_id = 0
    
    try:
        # Open file for reading
        with open(file, 'r') as file:
            
            # Read header line and skip
            file.readline()
            for line in file:
                split_line = line.split()
                
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
                
        return interaction_dict

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)




def write_dict_to_csv(gene_dict, filename, weight_min):
    with open(filename, 'w') as out:
        # Write header
        out.write("this_gene,other_gene,weight\n")
        
        # Write each entry
        for (gene1, gene2), weight in gene_dict.items():
            if weight >= weight_min:
                out.write(f"{gene1},{gene2},{weight}\n")
    return






def run_processing(weight_min):
    """Function that runs above functions while asking for input"""
    
    # Sort tmpfile
    tmpfile = "data/tmpfile"
    sorted_tmpfile = "data/sorted_tmpfile"
    sort_file(tmpfile, sorted_tmpfile)
    
    # Make edge_dict from sorted_tmpfile
    edge_dict = put_in_dict(sorted_tmpfile)
    edge_dict = {k: v for k, v in sorted(edge_dict.items(), key=lambda item: item[1])}
    
    try:
        write_dict_to_csv(edge_dict, 'edge_table.csv', weight_min)
    
    except:
        print(f"Usage: python {sys.argv[0]}(weight_min)")
        sys.exit(1)


if __name__ == "__main__":
    try:
        weight_min = int(input("Please write a minimum weight: "))
    except ValueError: 
        print("Error: weight_min must be a number")
        sys.exit(1)
    
    run_processing(weight_min)