# Importing libraries
import sys

# Importing functions from other files
from importData import import_data
from createEdgefile import create_edge_file
from createNodefile import create_node_file
from createGraph import create_graph

# Ask for user input
while True:
        try:
            tax_id_input = input("\nPlease enter a tax ID(or press Enter for 9606 as default): ").strip()
            tax_id = int(tax_id_input) if tax_id_input else 9606
            break
        except ValueError:
            print("Error: Tax ID must be a number. Please try again.")

while True:
        try:
            weight_min_input = input("\nPlease enter a minimum weight (or press Enter for 3 as default): ").strip()
            weight_min = int(weight_min_input) if weight_min_input else 3
            break
        except ValueError: 
            print("Error: weight_min must be a number. Please try again.")
        
while True:
        try:
            n_degree_input = input("\nPlease enter a minimum degree (or press Enter for 2 as default): ").strip()
            n_degree = int(n_degree_input) if n_degree_input else 2
            break
        except ValueError:
            print("Error: Minimum degree must be a number. Please try again.")
    
while True:
    try:
        n_hubs_input = input("\nPlease enter the number of top hubs (or press Enter for 3 as default): ").strip()
        n_hubs = int(n_hubs_input) if n_hubs_input else 3
        break
    except ValueError:
        print("Error: Number of top hubs must be a number. Please try again.")


# Ask user for file paths or use defaults
input_file = input("Please enter the path to gene2pubmed.gz (or press Enter for default): ").strip() or 'data/downloaded/gene2pubmed.gz'
tmp_file = input("Please enter the path to temporary output file (or press Enter for default): ").strip() or "data/tmp_file.tsv"
sorted_tmp_file = input("Please enter the path to sorted temporary file (or press Enter for default): ").strip() or "data/sorted_tmp_file.tsv"
edge_file = input("Please enter the path to edge_table.csv (or press Enter for default): ").strip() or 'data/edge_table.csv'
node_file = input("Please enter the path to node_table.csv (or press Enter for default): ").strip() or 'data/node_table.csv'
info_file = input("Please enter the path to gene_info.gz (or press Enter for default): ").strip() or "data/downloaded/gene_info.gz"

# Import Data
import_data(tax_id, input_file, tmp_file)

# Create Edge File
create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min)

############################
# Unit tests

# Create Node File
create_node_file(edge_file, node_file, tax_id, info_file)

# Run in Cytoscape
create_graph(edge_file, node_file, n_degree, n_hubs)
