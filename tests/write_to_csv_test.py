import pytest
import sys
from pathlib import Path
import gzip

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from createEdgefile import write_dict_to_csv

@pytest.fixture
def create_test_dict():
    """Fixture to create a sample gene dictionary"""
    test_dict = {
        ('Gene1', 'Gene2'): 5,
        ('Gene1', 'Gene3'): 3,
        ('Gene2', 'Gene3'): 1,
        ('Gene4', 'Gene5'): 10,
    }
    return test_dict

def test_write_dict_to_csv_1(create_test_dict, tmp_path):
    # Arrange
    test_dict = create_test_dict
    edge_file = tmp_path / "edges.csv"
    weight_min = 2
    
    # Act
    write_dict_to_csv(test_dict, str(edge_file), weight_min)
    
    # Assert
    with open(edge_file, 'r') as f:
        result = f.read()
        expected = "this_gene,other_gene,weight\nGene1,Gene2,5\nGene1,Gene3,3\nGene4,Gene5,10\n"
        assert result == expected, f"Did not get expected output"

def test_write_dict_to_csv_2(tmp_path):
    # Arrange
    test_dict = {}
    edge_file = tmp_path / "empty_edges.csv"
    weight_min = 1
    
    # Act
    write_dict_to_csv(test_dict, str(edge_file), weight_min)
    
    # Assert
    with open(edge_file, 'r') as f:
        result = f.read()
        expected = "this_gene,other_gene,weight\n"
        assert result == expected, f"Expected an empty CSV with header, but got:{result}"