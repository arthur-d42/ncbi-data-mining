import pytest
import sys
from pathlib import Path
import gzip

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from importData import import_data

@pytest.fixture
def create_test_file(tmp_path):
    # Create a test file
    input_file = tmp_path / "test_file.gz"
    with gzip.open(input_file, 'wb') as f: 
        f.write(b"#Header line\n")
        f.write(b"9606\t1234\tPubMed1\n")
        f.write(b"9606\t5678\tPubMed2\n")
        f.write(b"10090\t9101\tPubMed3\n")
    
    tmp_file = tmp_path / "output.txt"
    return str(input_file), str(tmp_file)


def test_ImportData_1(create_test_file):
    # Arrange
    input_file, tmp_file = create_test_file
    tax_id = "9606"
    
    # Act
    count = import_data(tax_id, input_file, tmp_file)
    
    # Assert
    assert count == 2, "Imported wrong number of lines for the tax_id"


def test_ImportData_2(create_test_file):
    # Arrange
    input_file, tmp_file = create_test_file
    tax_id = "9606"
    
    # Act
    count = import_data(tax_id, input_file, tmp_file)
    
    # Assert
    with open(tmp_file, 'r') as file: 
        output = file.read()
        expected_output = "#Header line\n9606\t1234\tPubMed1\n9606\t5678\tPubMed2\n"
        assert output == expected_output, "Wrote wrong output"


def test_ImportData_3(create_test_file):
    # Arrange
    input_file, tmp_file = create_test_file
    tax_id = "Invalid tax_id"
        
    # Act & Assert
    with pytest.raises(SystemExit) as excinfo:
        import_data(tax_id, input_file, tmp_file)
    assert str(excinfo.value) == "1", "Did not get correct error code"