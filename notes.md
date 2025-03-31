
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

We can reasonably expect the humand dataset to be one of if not the largest so by filtering these we already reduce the dataset by a factor of >30




What kind of interesting and informative networks can be created by filtering or selection?:

### A network with many connected nodes = many genes.
maybe have a cutoff filtering? Like less than 3 connections is not strong enought?

### Networks where the sum of the edges is high = many co-mentioning articles.

### High edge-sum/nodes = high importance of the network, many articles.
Some nodes in the graph do not have any connecting edges = virgin territory or maybe uninteresting.
Networks that consists of only few nodes where the connecting edges have low weights = not much research has been made.
Networks that connect to a specific gene = an overview of a interaction network, maybe a biological process.
Networks that has a specific gene as a center and has connections to the n'th degree (star shaped).