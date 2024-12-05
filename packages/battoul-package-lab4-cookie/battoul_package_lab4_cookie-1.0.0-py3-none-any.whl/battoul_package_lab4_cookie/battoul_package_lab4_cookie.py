import csv
from row_2_list import row_to_list  # Import the function to be tested
import pytest



# Load your dataset from the CSV file
dataset = []
with open('<path_to_your_house_price.csv>', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        dataset.append(row)

# Test if the function correctly handles rows with missing values
# Parametrize the test function to iterate through each row in the dataset
@pytest.mark.parametrize("input_row", dataset)
def test_row_to_list_with_missing_values(input_row):
    input_string = ' '.join(input_row)  # Convert list to string
    #Complete the function to assert if any missing value is found in your input_string