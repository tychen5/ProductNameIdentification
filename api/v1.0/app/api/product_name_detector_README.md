# Product Name Detector

This Python script, `product_name_detector.py`, processes and filters product names from a given dataset. The script is designed to work with data from a Tableau server and a Shopify export file. It utilizes the GloVe model for natural language processing and performs various operations to filter and process the product names.

### Features

- Connects to a Tableau server and retrieves relevant data.
- Processes and filters product names using the GloVe model.
- Removes stop words and bad tokens from the product names.
- Appends spaces to tokens with a length less than or equal to 5.
- Constructs a list of unique sets from the processed product names.
- Saves the final processed DataFrame to a pickle file.

### Dependencies

- pandas
- numpy
- pickle
- datetime
- itertools
- re
- string
- inflect
- collections
- tableau_api_lib

### Usage

1. Ensure that all dependencies are installed.
2. Replace the placeholder paths in the script with the actual paths to your data files, GloVe model file, and stop words file.
3. Run the script using a Python interpreter.

### Functions

- `load_glove_model(file_path)`: Loads the GloVe model from a file and returns a list of words in the model.
- `filter_out_bad_set(ori_set, bad_set)`: Filters out bad tokens from the original set and appends spaces to tokens with a length less than or equal to 5.
- `construct_detect_di(lilili)`: Takes a list of lists of lists and returns a list of unique sets created from the innermost lists.

### Output

The script saves the final processed DataFrame to a pickle file with the filename `productline_keywords_df.pkl`.