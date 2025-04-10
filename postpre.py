import subprocess


def sort_file(input_file, output_file):
    # Sort based on 3 column, and 3 column only. 
    # It is sorted as a number, which leaves header at the top and a more logical flow so that 124 will be higher than 13
    subprocess.run(["sort", "-k3,3n", input_file, "-o", output_file])
    return


def put_in_dict(file):
    # Creates dict for data storage
    interaction_dict = {}
    current_genes = []
    current_id = 0
    
    # Open file for reading
    with open(file, 'r') as file:
        for line in file:
            
            # Read header line and skip
            file.readline()
            
            split_line = line.split()
            
            pubmed_id = split_line[2]
            gene = split_line[1]
            
            #first id
            if current_pubmed_id == 0:
                current_pubmed_id = pubmed_id

            if pubmed_id == current_pubmed_id:
                current_genes.append(gene)
                
            else:
                # Put every set of genes up
                for this_gene in current_genes:
                    for other_gene in current_genes:
                        if this_gene != other_gene:
                            edge = (this_gene, other_gene)
                            
                            if not interaction_dict[edge]:
                                interaction_dict.update[edge:1]
                            else: 
                                interaction_dict[edge] += 1    
                current_pubmed_id = pubmed_id
                current_genes = [gene]
            
    return interaction_dict


tmpfile = "data/tmpfile"
sorted_tmpfile = "data/sorted_tmpfile"

sort_file(tmpfile, sorted_tmpfile)

print(put_in_dict(sorted_tmpfile))
