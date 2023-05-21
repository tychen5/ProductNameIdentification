# Product Line Conversion

This Python script, `product_line_conversion.py`, is designed to process and convert product names and SKUs into their respective product lines. The script reads data from an Excel file and a pickled file, processes the data, and generates two pickled dictionaries as output. These dictionaries can be used to map product names and SKUs to their corresponding product lines.

### Dependencies

- Python 3.6+
- pandas
- pickle
- itertools

### Usage

1. Ensure that the required dependencies are installed.
2. Replace `/path/to/your/data/` in the script with the actual path to your data folder.
3. Run the script using `python product_line_conversion.py`.

### How it works

The script performs the following steps:

1. Imports the necessary libraries.
2. Defines a function `convert2pl()` that converts a first-level string to a product line using a predefined dictionary `fl_convert_dict`.
3. Reads data from a pickled file containing product line information and an Excel file containing product name revisions.
4. Processes the data to create two dictionaries: `newadd_name` and `baddel_name`, which store new product names and bad product names, respectively.
5. Creates a dictionary `detect_di` that maps product names and SKUs to their corresponding product lines, filtering out bad product names.
6. Saves the `detect_di` dictionary as a pickled file named `reverse_pn2pl_di.pkl`.
7. Repeats steps 4-6 for lowercase product names and saves the resulting dictionary as a pickled file named `reverse_pn2pl_di_lowercase.pkl`.

### Output

The script generates two pickled dictionaries:

- `reverse_pn2pl_di.pkl`: A dictionary that maps product names and SKUs to their corresponding product lines.
- `reverse_pn2pl_di_lowercase.pkl`: A dictionary that maps lowercase product names and SKUs to their corresponding product lines.