# Importing functions from other files
from importData import run_import_gene2pubmed
from processData import run_processing
from addName import geneID_to_symbol_dict


# Importing data into tmp file for less use of memory 
run_import_gene2pubmed()

weight_min = input("Please write a minimum weight: ")

# Testing
run_processing(weight_min)


# Testing 2

