#!/usr/bin/env python3
import sys
import pathlib
import gzip

def import_data(tax_id, input_file):
    # Relative file fixthis 
    tmp_file = "data/tmpfile"
    filename = input_file
    # Open with gzip.open!!
    with gzip.open(filename, 'rb') as file, open(tmp_file, 'w') as tmp:
        # First line
        first_line = file.readline().decode("utf-8")
        # readline() adds \n for us maybe?
        tmp.write(f"{first_line}")
        # The rest of the lines
        for line in file:
            # Convert form byte to string
            line = line.decode("utf-8")
            line = line.strip()
            if line.startswith(f"{tax_id}\t"):
                tmp.write(f"{line}\n")
    file.close()
    tmp.close()

def main():
    tax_id = sys.argv[1]
    input_file = sys.argv[2]
    import_data(tax_id, input_file)

try:
    # Asks user for a positive integer
    tax_id = input("Please a tax_id: ")
    input_file = 'data/downloaded/gene2pubmed.gz'
    
    # Calculates the factorial and prints results
    result = import_data(tax_id, input_file)
    print(f"Done")

except:
    print("Error")