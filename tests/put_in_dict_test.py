import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))

from createEdgefile import put_in_dict

def test_put_in_dict_1(tmp_path):
    # Arrange
    sorted_file = tmp_path / "complex_case.txt"
    with open(sorted_file, 'w') as f:
        f.write("#Header line\n")
        f.write("A\tGene1\t101\n")
        f.write("B\tGene2\t101\n")
        f.write("C\tGene3\t101\n")
        f.write("D\tGene4\t101\n")
        f.write("E\tGene1\t102\n")
        f.write("F\tGene2\t102\n")
        f.write("G\tGene3\t102\n")
    
    # Act
    result = put_in_dict(str(sorted_file))
    
    # Assert
    expected = {
        ('Gene1', 'Gene2'): 2,
        ('Gene1', 'Gene3'): 2,
        ('Gene2', 'Gene3'): 2,
        ('Gene1', 'Gene4'): 1,
        ('Gene2', 'Gene4'): 1,
        ('Gene3', 'Gene4'): 1
    }
    assert result == expected, f"Got different output than expected"

def test_put_in_dict_2(tmp_path):
    # Arrange
    sorted_file = tmp_path / "empty.txt"
    sorted_file.touch()  # Create an empty file
    
    # Act
    result = put_in_dict(str(sorted_file))
    
    # Assert
    assert result == {}, "Expected an empty dictionary for an empty input file"