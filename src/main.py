# Importing libraries
import sys
import os

# Importing functions from other files
from importData import file_exists
from importData import import_data
from createEdgefile import create_edge_file
from createNodefile import create_node_file
from createGraph import create_graph

# Ask for user input
while True:
        try:
            tax_id_input = input("\nPlease enter a tax ID (or press Enter for 69 as default): ").strip()
            tax_id = int(tax_id_input) if tax_id_input else 69
            break
        except ValueError:
            print("Error: Tax ID must be a number. Please try again.")

while True:
        try:
            weight_min_input = input("\nPlease enter the minimum weight of the edges you want (or press Enter for 3 as default): ").strip()
            weight_min = int(weight_min_input) if weight_min_input else 3
            break
        except ValueError: 
            print("Error: weight_min must be a number. Please try again.")
        
while True:
        try:
            n_degree_input = input("\nPlease enter the minimum degree of the nodes you want (or press Enter for 2 as default): ").strip()
            n_degree = int(n_degree_input) if n_degree_input else 2
            break
        except ValueError:
            print("Error: Minimum degree must be a number. Please try again.")
    
while True:
    try:
        n_hubs_input = input("\nPlease enter the number of top hubs you want displayed (or press Enter for 3 as default): ").strip()
        n_hubs = int(n_hubs_input) if n_hubs_input else 3
        break
    except ValueError:
        print("Error: Number of top hubs must be a number. Please try again.")


# Ask user for file paths or use defaults
while True:
    input_file = input("\nPlease enter the path to the gene2pubmed file (or press Enter for default): ").strip() or "data/downloaded/gene2pubmed.gz"
    if file_exists(input_file):
        break
    print(f"Error: Input file '{input_file}' not found. Please try again.")

while True:
    info_file = input("\nPlease enter the path to the gene info file (or press Enter for default): ").strip() or "data/downloaded/gene_info.gz"
    if file_exists(info_file):
        break
    print(f"Error: Info file '{info_file}' not found. Please try again.")


tmp_file = input("\nPlease enter where you want the temporary file (or press Enter for default): ").strip() or "data/tmp_file.tsv"
sorted_tmp_file = input("\nPlease enter where you want the sorted temporary file (or press Enter for default): ").strip() or "data/sorted_tmp_file.tsv"
edge_file = input("\nPlease enter where you want the edge file (or press Enter for default): ").strip() or 'data/edge_table.csv'
node_file = input("\nPlease enter where you want the node file (or press Enter for default): ").strip() or 'data/node_table.csv'


# Import Data
import_data(tax_id, input_file, tmp_file)

# Create Edge File
create_edge_file(tmp_file, sorted_tmp_file, edge_file, weight_min)


# Delete temporary files
try:
    os.remove(tmp_file)
    print(f"Temporary file '{tmp_file}' deleted.")
    os.remove(sorted_tmp_file)
    print(f"Sorted temporary file '{sorted_tmp_file}' deleted.")
except FileNotFoundError:
    print("Error: One or both temporary files not found.")
except PermissionError:
    print("Error: Permission denied while trying to delete temporary files.")
except Exception as e:
    print(f"An unexpected error occurred while deleting temporary files: {e}")



# Create Node File
create_node_file(edge_file, node_file, tax_id, info_file)

# Run in Cytoscape
create_graph(edge_file, node_file, n_degree, n_hubs)
