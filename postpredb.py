import subprocess, sqlite3

def sort_file(input_file, output_file):
    # Sort based on 3 column, and 3 column only. 
    # It is sorted as a number, which leaves header at the top and a more logical flow so that 124 will be higher than 13
    subprocess.run(["sort", "-k3,3n", input_file, "-o", output_file])
    # add placeholder line at end to make the open 'r' loop run for the last line
    with open(output_file, 'a') as f:
        f.write("x\tx\tx\n")
    return


def put_in_db(sorted_file):
    current_genes = []
    current_pubmed_id = 0
    #           pubmed_id1 pubmed_id2 pubmed_id3
    # pubmed_id1    x       x           x
    # pubmed_id2    1       x           x
    # pubmed_id3    2       0           x
    #                                    \   everything above this line
    #                                     \  will not be kept with the set
    #                                      \ as key approach
    # Open file for reading
    con = sqlite3.connect("tmp.db")
    cur = con.cursor()

    # Is this even allowed we're just using bash and sql commands
    cur.execute("DROP TABLE IF EXISTS interaction_dict")
    cur.execute('''
    CREATE TABLE interaction_dict(
        gene1 TEXT,
        gene2 TEXT,
        count INTEGER,
        PRIMARY KEY (gene1, gene2)
    )
    ''')
    with open(sorted_file, 'r') as file:
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
                
            # When found next pubmed article we process the previous one
            else:
                # This ensures consistent ordering of genes
                # If not done we might get a set of (21,22) AND (22,21)
                current_genes.sort()
                for i in range(len(current_genes)):
                    this_gene = current_genes[i]
                    for other_gene in current_genes[i+1:]:
                        edge = (this_gene, other_gene)
                        # This is quite slow but it conserves memory
                        cur.execute('''
                        INSERT INTO interaction_dict (gene1, gene2, count)
                        VALUES (?, ?, 1)
                        ON CONFLICT(gene1, gene2)
                        DO UPDATE SET count = count +1
                        ''', edge)
                # Next pubmed_id
                con.commit()
                current_pubmed_id = pubmed_id
                # Add this gene to start the list
                current_genes = [gene]

    # close the db
    con.close()
    return con




def write_to_file(edge_dict, outfile):
    with open(outfile, 'w') as out:
        out.write(edge_dict)
    return


tmpfile = "data/smltmp"
sorted_tmpfile = "data/sorted_tmpfile"

sort_file(tmpfile, sorted_tmpfile)
put_in_db(sorted_tmpfile)

#write_to_file(put_in_dict(sorted_tmpfile))
