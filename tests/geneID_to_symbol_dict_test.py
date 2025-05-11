import pytest
import sys
import gzip
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from createNodefile import geneID_to_symbol_dict

@pytest.fixture
def create_tmp_file():
    tax_id = 9606 
    content = (
        f"{tax_id}\t1234\tTP53\n"
        f"{tax_id}\t5678\tBRCA1\n"
        "10090\t1111\tMdm2\n"
    )

    file_path = "tmp_gene_info.gz"
    with gzip.open(file_path, 'wt') as f:
        f.write(content)
    
    yield file_path
    
    Path(file_path).unlink(missing_ok=True)


def test_geneID_to_symbol_dict_1(create_tmp_file):
    # Arrange
    tax_ID = 9606
    
    # Act
    result = geneID_to_symbol_dict(tax_ID, create_tmp_file)
    
    # Assert
    expected_output = {'1234': 'TP53', '5678': 'BRCA1'}
    assert result == expected_output, "Test of simple scenario" 
    


def test_geneID_to_symbol_dict_2(create_tmp_file):
    # Arrange
    tax_ID = 666 #non-existing tax ID
    
    # Act
    result = geneID_to_symbol_dict(tax_ID, create_tmp_file)
    
    # Assert
    expected_output = {}
    assert result == expected_output, "Test of non-existing tax ID"