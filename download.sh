#!/usr/bin/env bash
mkdir -p data/downloaded
cd data/downloaded
wget https://ftp.ncbi.nih.gov/gene/DATA/gene2pubmed.gz
wget https://ftp.ncbi.nih.gov/gene/DATA/gene_info.gz
