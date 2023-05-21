product_line_conversion.py

# README.md

## Product Line Conversion

This Python script, `product_line_conversion.py`, is designed to process and convert product names and SKUs into their respective product lines. The script reads data from an Excel file and a pickle file, processes the data, and saves the results as two new pickle files.

### Dependencies

- Python 3.x
- pandas
- pickle
- itertools

### Usage

1. Replace the dummy paths and variables in the script with your actual data paths and variables.
2. Run the script using `python product_line_conversion.py`.

### Functions

- `convert2pl(flstr)`: Converts a first-level string to a product line using a predefined dictionary.

### Workflow

1. The script imports necessary libraries and defines the `convert2pl` function.
2. It reads data from a pickle file and an Excel file, and processes the data to create dictionaries for new and bad product names.
3. The script filters out bad product names and creates a dictionary to map product names and SKUs to their respective product lines.
4. The results are saved as two new pickle files: `reverse_pn2pl_di.pkl` and `reverse_pn2pl_di_lowercase.pkl`.

### Input Data

- `bigrule_pl.pkl`: A pickle file containing product line information.
- `Product_name_revision.xlsx`: An Excel file containing product names and bad product names.

### Output Data

- `reverse_pn2pl_di.pkl`: A pickle file containing the mapping of product names and SKUs to their respective product lines.
- `reverse_pn2pl_di_lowercase.pkl`: A pickle file containing the mapping of lowercase product names and SKUs to their respective product lines.