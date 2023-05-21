# Product Data Processing

This Python script processes product data from various sources, including Tableau server, Shopify, and Excel files, to create a comprehensive dictionary of product names and their corresponding product lines. The script also filters out bad entries and cleans the data to ensure accuracy and consistency.

### Dependencies

- pandas
- numpy
- pickle
- re
- string
- collections
- tableau_api_lib

### Usage

1. Ensure that all required dependencies are installed.
2. Replace the placeholders in the `tableau_server_config` dictionary with your own credentials and server URL.
3. Replace the data paths in the script with the appropriate paths to your data files.
4. Run the script to process the data and generate the output files.

### Key Functions

- `convert2pl(flstr)`: Converts a first-level string to a product line using the `fl_convert_dict` dictionary.
- Data processing: The script loads data from various sources, processes it, and merges it into a single DataFrame.
- Data cleaning: The script filters out bad entries and cleans the data to ensure accuracy and consistency.
- Dictionary creation: The script creates a dictionary of product names and their corresponding product lines, filtering out bad names and adding new names from the Excel file.

### Output Files

- `reverse_pn2pl_di.pkl`: A pickle file containing the dictionary of product names and their corresponding product lines.
- `reverse_pn2pl_di_lowercase.pkl`: A pickle file containing the dictionary of product names (in lowercase) and their corresponding product lines.

### Note

Please ensure that you replace the dummy paths and examples with your actual data paths and credentials before running the script.