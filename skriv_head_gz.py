import gzip

filepath = "data/downloaded/gene_info.gz"

# Look for specific tax_id
target_tax_id = input("Please write a tax_id: ").strip()

# Open file, and read header and two first lines for that tax_id:
with gzip.open(filepath, 'rt') as f:
    header = f.readline().strip().lstrip('#').split('\t')
    
    matching_rows = []
    for line in f:
        fields = line.strip().split('\t')
        if fields[0] == target_tax_id:
            matching_rows.append(fields)
        if len(matching_rows) == 2:
            break

# If two rows is found, it is printed with the header:
if len(matching_rows) == 2:
    row1, row2 = matching_rows
    for name, val1, val2 in zip(header, row1, row2):
        print(f"{name:<20}\t{val1:<15}\t{val2}")
# Otherwise:
else:
    print(f"Only found {len(matching_rows)} rows with tax_id {target_tax_id}.")
