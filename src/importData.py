#!/usr/bin/env python3
# Import libraries
import sys
import pathlib
import gzip

def import_data(tax_id, input_file, tmp_file):
    """Function that imports the data from an organism with a specified tax_id from the gene2pubmed into a temp-file"""
    # Relative file fixthis 
    count = 0
    
    if not tax_id.isdigit():
        print(f"Error: tax_id must be a number. You entered: '{tax_id}'")
        sys.exit(1)
    
    try:
        # Checking whether input file exists
        if not pathlib.Path(input_file).is_file():
            raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

        # Open with gzip.open
        with gzip.open(input_file, 'rb') as file, open(tmp_file, 'w') as tmp:
            # First line
            first_line = file.readline().decode("utf-8")
            tmp.write(f"{first_line}")
            # The rest of the lines
            for line in file:
                # Convert form byte to string
                line = line.decode("utf-8")
                line = line.strip()
                if line.startswith(f"{tax_id}\t"):
                    tmp.write(f"{line}\n")
                    count += 1
        
        # Printing warning if no lines found for tax_id
        if count == 0:
            print(f"Warning: No entries found for tax_id {tax_id}")
        
        # End of function
        print(f"Done importing file\nNumber of lines: {count}")
        return count
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def run_import_data(tax_id, input_file, tmp_file):
    import_data(tax_id, input_file, tmp_file)
    return tax_id




# For running this function seperately in terminal
def main():
    """Function that runs import_data() while asking for input"""
    if len(sys.argv) == 1:
        # If just file is called
        tax_id = input("Please write a tax_id: ")
        if not tax_id.isdigit():
            print(f"Error: tax_id must be a number. You entered: '{tax_id}'")
            sys.exit(1)
        
        input_file = input(f"Please enter the path to gene2pubmed.gz\nIf clicking \"Enter\", default is data/downloaded/gene2pubmed.gz: ").strip()
        if not input_file:
            input_file = "data/downloaded/gene2pubmed.gz"
            
        import_data(tax_id, input_file)
        return tax_id
    
    elif len(sys.argv) == 2:
        # One argument: tax_id (uses standard location of gene2pubmed)
        tax_id = sys.argv[1]
        if not tax_id.isdigit():
            print(f"Error: tax_id must be a number. You entered: '{tax_id}'")
            sys.exit(1)
            
        input_file = input(f"Please enter the path to gene2pubmed.gz\nIf clicking \"Enter\", default is data/downloaded/gene2pubmed.gz: ").strip()
        if not input_file:
            input_file = "data/downloaded/gene2pubmed.gz"
        
        import_data(tax_id, input_file)
        return tax_id
        
    elif len(sys.argv) == 3: 
        # If both program, tax_id and file is provided
        tax_id = sys.argv[1]
        input_file = sys.argv[2]
        import_data(tax_id, input_file)
        return tax_id
    
    else:
        print(f"Usage: python {sys.argv[0]} tax_id(optional) dir_to_gene2pubmed.gz(optional)")
        sys.exit(1)

if __name__ == "__main__":
    main()