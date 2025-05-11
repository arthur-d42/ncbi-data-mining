import pytest
import sys
import gzip
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from createNodefile import create_node_file

@pytest.fixture
def create_edge_file(tmp_path):
    edge_content = (
        "this_gene,other_gene,weight\n"
        "Gene1,Gene2,5\n"
        "Gene1,Gene3,3\n"
        "Gene4,Gene5,10\n"
        )
    
    edge_file = tmp_path / "edge_file.csv"
    edge_file.write_text(edge_content)
    return edge_file

@pytest.fixture
def create_info_file(tmp_path):
    tax_id = 9606
    info_content = (
        f"{tax_id}\tGene1\tTP53\n"
        f"{tax_id}\tGene2\tBRCA1\n"
        f"{tax_id}\tGene3\tEGFR\n"
        f"{tax_id}\tGene4\tMYC\n"
        f"{tax_id}\tGene5\tAPC\n"
        )
    
    info_file = tmp_path / "gene_info.gz"
    
    with gzip.open(info_file, 'wt') as file:
        file.write(info_content)
    return info_file

def test_create_node_file_1(tmp_path, create_edge_file, create_info_file):
    # Arrange
    edge_file = create_edge_file
    node_file = tmp_path / "nodes.csv"
    tax_id = 9606
    info_file = create_info_file
    
    # Act
    create_node_file(edge_file, node_file, tax_id, info_file)
    
    # Assert
    with open(node_file, 'r') as file:
        result = file.read()
        expected = (
        "geneID,symbol\n"
        "Gene1,TP53\n"
        "Gene2,BRCA1\n"
        "Gene3,EGFR\n"
        "Gene4,MYC\n"
        "Gene5,APC\n"
        )
        assert result == expected, "Creation of simple node file"
        
        

def test_create_node_file_2(tmp_path):
    # Arrange
    empty_edge_file = tmp_path / "empty_edges.csv"
    empty_edge_file.write_text("this_gene,other_gene,weight\n")
    node_file = tmp_path / "nodes.csv"
    tax_id = 9606
    info_file = tmp_path / "gene_info.gz"
    
    with gzip.open(info_file, 'wt') as file:
        file.write("9606\tGene1\tTP53\n")
    
    # Act
    create_node_file(empty_edge_file, node_file, tax_id, info_file)
    
    # Assert
    with open(node_file, 'r') as file:
        result = file.read()
        expected = ("geneID,symbol\n")
        assert result == expected, "Check with empty edge file"
    
