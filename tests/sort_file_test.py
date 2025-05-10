import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from createEdgefile import sort_file

@pytest.fixture
def create_test_file(tmp_path):
    # Create a test file with unsorted data
    input_file = tmp_path / "unsorted.txt"
    sorted_file = tmp_path / "sorted.txt"
    with open(input_file, 'w') as f:
        f.write("#Header line\n")
        f.write("A\t1\t124\n")
        f.write("B\t2\t13\n")
        f.write("C\t3\t124\n")
        f.write("D\t4\t12\n")
    return str(input_file), str(sorted_file)

def test_sort_file_1(create_test_file):
    # Arrange
    input_file, sorted_file = create_test_file
    
    # Act
    sort_file(input_file, sorted_file)
    
    # Assert
    with open(sorted_file, 'r') as f:
        result = f.read()
        expected = "#Header line\nD\t4\t12\nB\t2\t13\nA\t1\t124\nC\t3\t124\n" #Output that is sorted on column 3 and then column 2
        assert result == expected, "Sorted file does not match expected output"

def test_sort_file_2(tmp_path):
    # Arrange
    input_file = tmp_path / "empty.txt"
    sorted_file = tmp_path / "sorted_empty.txt"
    input_file.touch()  # Create an empty file
    
    # Act
    sort_file(str(input_file), str(sorted_file))
    
    # Assert
    with open(sorted_file, 'r') as f:
        result = f.read()
        assert result == "", "Empty input file should result in an empty output file"