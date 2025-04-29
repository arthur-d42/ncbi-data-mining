import subprocess
from collections import OrderedDict
from operator import itemgetter
 
def sort_dict_by_value(test_dict):
    sorted_list = sorted(test_dict.items(), key=itemgetter(1))
    return OrderedDict(sorted_list)

def sort_file(input_file, output_file):
    # Sort based on 3 column, and 3 column only. 
    # It is sorted as a number, which leaves header at the top and a more logical flow so that 124 will be higher than 13
    subprocess.run(["sort", "-k3,3n", "-k2,2n", input_file, "-o", output_file])
    return


def put_in_dict(file):
    # Creates dict for data storage
    interaction_dict = {}
    current_genes = []
    current_pubmed_id = 0
    
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
                if len(current_genes) >= 1000:
                    interaction_dict[pubmed_id] = [len(current_genes), current_genes]


                current_pubmed_id = pubmed_id
                # because the "read pointer" is actually on the next line when all of the above is running
                current_genes = [gene]
    return interaction_dict


tmpfile = "data/tmpfile"
sorted_tmpfile = "data/sorted_tmpfile"

sort_file(tmpfile, sorted_tmpfile)
edge_dict = put_in_dict(sorted_tmpfile)
# write_to_file(put_in_dict(sorted_tmpfile), "data/edges")
