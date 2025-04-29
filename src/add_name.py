import gzip

def geneID_to_symbol_dict(taxID):
    filepath = "data/downloaded/gene_info.gz"
    
    symbol_dict = {}
    
    with gzip.open(filepath, 'rt') as file:
        for line in file:
            split_line = line.split()
            if split_line[0] == taxID:
                geneID = split_line[1]
                symbol = split_line[2]
                symbol_dict[geneID] = symbol
        
        file.close()    
        return symbol_dict
