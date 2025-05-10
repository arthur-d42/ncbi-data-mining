#!/usr/bin/env python3
# Import libraries
import sys
import pathlib
import gzip

def import_data(tax_id, input_file, tmp_file):
    """Function that imports the data from an organism with a specified tax_id from the gene2pubmed into a temp-file""" 
    count = 0
    
    print("Starting import of data")
    
    try:
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
            sys.exit(1)
        
        # End of function
        print(f"Done importing file\nNumber of lines: {count}")
        return count
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    except PermissionError as e:
        print(f"Error: Permission denied when writing to '{tmp_file}'. {e}")
        sys.exit(1)
    
    except gzip.BadGzipFile:
        print(f"Error: The file '{input_file}' is not a valid gzip file.")
        sys.exit(1)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    """Function that runs import_data() while asking for input"""
    while True:
        try:
            tax_id_input = input("\nPlease enter a tax ID(or press Enter for 9606 as default): ").strip()
            tax_id = int(tax_id_input) if tax_id_input else 9606
            break
        except ValueError:
            print("Error: Tax ID must be a number. Please try again.")
            
    input_file = input(f"Please enter the path to gene2pubmed.gz (or press Enter for default): ").strip() or "data/downloaded/gene2pubmed.gz"
        
    tmp_file = input("Please enter the path to temporary output file (or press Enter for default): ").strip() or "data/tmp_file.tsv"
    
    import_data(tax_id, input_file, tmp_file)
    return tax_id

if __name__ == "__main__":
    # For running the program in terminal
    main()