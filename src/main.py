# Importing libraries
import sys


# Importing functions from other files
from importData import import_data
from createEdgefile import create_edge_file
from createNodefile import create_node_file
from grapProcessing import *

# Ask for user input
try:
    tax_id = input("Please write a tax_id: ")
    if not tax_id.isdigit():
        raise ValueError("tax_id must be a number.")
except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)

try:
    weight_min = int(input("Please write a minimum weight (suggestion is 1): "))
except ValueError: 
    print("Error: weight_min must be a number")
    sys.exit(1)


# Ask user for file paths or use defaults
input_file = input("Enter path to gene2pubmed.gz (or press Enter for default): ").strip()
if not input_file:
    input_file = 'data/downloaded/gene2pubmed.gz'

tmp_file = input("Enter path to temporary output file (or press Enter for default): ").strip()
if not tmp_file:
    tmp_file = "data/tmp_file.tsv"

sorted_tmp_file = input("Enter path to sorted temporary file (or press Enter for default): ").strip()
if not sorted_tmp_file:
    sorted_tmp_file = "data/sorted_tmp_file.tsv"

edge_file = input("Enter path to edge_table.csv (or press Enter for default): ").strip()
if not edge_file:
    edge_file = 'data/edge_table.csv'

node_file = input("Enter path to node_table.csv (or press Enter for default): ").strip()
if not node_file:
    node_file = 'data/node_table.csv'

info_file = input("Enter path to gene_info.gz (or press Enter for default): ").strip()
if not info_file:
    info_file = "data/downloaded/gene_info.gz"




# Import Data
import_data(tax_id, input_file, tmp_file)


# Create Edge File
create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min)


# Create Node File
create_node_file(edge_file, node_file, tax_id, info_file)
