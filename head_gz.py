import gzip

filepath = "data/downloaded/gene_info.gz"

with gzip.open(filepath, 'rt') as f:
    header = f.readline().strip().lstrip('#').split('\t')
    line1 = f.readline().strip().split('\t')
    line2 = f.readline().strip().split('\t')

# Print header and first two rows
for name, val1, val2 in zip(header, line1, line2):
    print(f"{name:<20}\t{val1:<15}\t{val2}")
