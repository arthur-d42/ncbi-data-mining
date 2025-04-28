import subprocess
import tracemalloc
import time

# Start timing and memory monitoring
start_time = time.time()
tracemalloc.start()


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


def write_to_file(edge_dict, outfile):
    with open(outfile, 'w') as out:
        out.write(edge_dict)
    return


tmpfile = "data/tmpfile"
sorted_tmpfile = "data/sorted_tmpfile"

sort_file(tmpfile, sorted_tmpfile)
edge_dict = put_in_dict(sorted_tmpfile)
# write_to_file(put_in_dict(sorted_tmpfile), "data/edges")
print(edge_dict)
print(f"Size of dict = {len(edge_dict)}")

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 10**6:.2f} MB")
print(f"Peak memory usage: {peak / 10**6:.2f} MB")

# Stop monitoring
current, peak = tracemalloc.get_traced_memory()
end_time = time.time()
execution_time = end_time - start_time

print(f"Current memory usage: {current / 10**6:.2f} MB")
print(f"Peak memory usage: {peak / 10**6:.2f} MB")
print(f"Execution time: {execution_time:.4f} seconds")

# Stop monitoring
tracemalloc.stop()
