#!/usr/bin/env python3
import sys
import pathlib
import gzip

def import_data(tax_id):
    # Relative file fixthis 
    tmp_file = "data/tmpfile"
    filename = "data/testdata2.gz"
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
            if line.startswith(tax_id):
                tmp.write(f"{line}\n")
    file.close()
    tmp.close()

def main():
    tax_id = sys.argv[1]
    import_data(tax_id)

if __name__ == "__main__":
    main()
