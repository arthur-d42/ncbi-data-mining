
# Program outline

## Preprocessing
### Concerns:
- high memory usage
### solution:
- Read file line by line
- Append every `tax id` to tmp file
#### Amount of genes for organisms
```sh
### all
zcat data/downloaded/gene2pubmed.gz | wc -l  
65568643
### Tax id 24:
zcat data/downloaded/gene2pubmed.gz |grep "^24\s" |  wc -l 
2805
#### Humans:
zcat data/downloaded/gene2pubmed.gz |grep "^9606\s" |  wc -l
2125321
```

We can reasonably expect the human dataset to be one of if not the largest so by filtering these we already reduce the dataset by a factor of >30




What kind of interesting and informative networks can be created by filtering or selection?:

## postpreprocessing
We need to make some kind of datastructure that's
- Efficient to loop through
- Doesn't take up too much memory space?
	- Generaetable 
**Could we do some sort of sorting of PubMed_ID?**
### Sorting of pubmed id
1. Sort descending order (O = log(n))
2. 
```python
interaction_dict = {123 : {1234:2, 12345:2}
					{1234: {123:2, 12345:1}	}
				{(123,12345):4
				"1234--123":5}

current_genes = []
for id:
	current_id = id

	# appends all the genes mentioned in current article
	if id = current_id:
		current_genes.append(line.gene)
	else
		for gene in current_genes:
			interaction_dict[genes].value += 1
			

# if key doesn't exist
[1,2,3,4]
sort(cg)
for i in range(len(cg)):
	# for everything after i
	this_gene = cg[i]
	for other_gene in cg[i+1:]:
		# current_gene is always smaller because sort earlier
		edge = (this_gene, other_gene)
		if not interaction_dict[edge]:
			interaction_dict.update{edge:1}
		else:
			# +1 to the value
			interaction_dict[edge] += 1
		
	
# On else statement (new id found)
current_genes[123,1234,12345]
123 vs [1234,12345]
1234 vs [12345]


	


def put_to_dict(infile)
	
```

### A network with many connected nodes = many genes.
maybe have a cutoff filtering? Like less than 3 connections is not strong enought?

### Networks where the sum of the edges is high = many co-mentioning articles.

### High edge-sum/nodes = high importance of the network, many articles.
Some nodes in the graph do not have any connecting edges = virgin territory or maybe uninteresting.
Networks that consists of only few nodes where the connecting edges have low weights = not much research has been made.
Networks that connect to a specific gene = an overview of a interaction network, maybe a biological process.
Networks that has a specific gene as a center and has connections to the n'th degree (star shaped).

# What to include?
## Is it reasonable to not include articles with > 1000 genes?

### article 12477934 has like 19 thousand genes
Looking at the article it links a protein to the uniprot database which links the protein to a whole lot of genes liek 6626 AND 6625 none of which are mentioned in the article sooo that's good




# Spørgsmål til Peter
- Hvor mange gener skal der i plottet?
- Hvad er den smarteste måde, at håndtere de store mængder af data
- Giver det mening bare at fjerne alt med over 1000 gener?

