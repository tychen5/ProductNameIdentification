# Data Preparation and Keywords Extraction

This Python script, `data_preparation_keywords.py`, contains functions that help in preparing data for further processing and extracting keywords from the given data using the Term Frequency-Inverse Document Frequency (TF-IDF) method.

### Functions

The script contains the following functions:

1. `prepare_data(final_product_df, target_col_name, explode_col_name, tcn_str=True)`

   This function prepares the data for further processing by filling missing values and finding keywords in the specified column.

   **Arguments:**
   - `final_product_df (DataFrame)`: Dataframe containing product information.
   - `target_col_name (str)`: Column name to fill missing values.
   - `explode_col_name (str)`: Column name to find keywords.
   - `tcn_str (bool, optional)`: If target column name's values are strings. Defaults to True.

   **Returns:**
   - `DataFrame`: Processed dataframe.

2. `construct_keywords(level_targetcolname_doc, target_col_name)`

   This function constructs unique terms using the TF-IDF method as keywords of the target_col_name.

   **Arguments:**
   - `level_targetcolname_doc (DataFrame)`: Dataframe containing target column name and document.
   - `target_col_name (str)`: Column name to fill missing values.

   **Returns:**
   - `dict`: Dictionary with keys as target_col_name(level's name) and values as a list of strings (explode_col_name's keywords).

### Usage

To use the functions in this script, simply import the required functions and pass the necessary arguments. For example:

```python
from data_preparation_keywords import prepare_data, construct_keywords

# Prepare the data
processed_data = prepare_data(final_product_df, 'target_column', 'explode_column')

# Construct keywords
keywords_dict = construct_keywords(processed_data, 'target_column')
```

This will return a processed dataframe and a dictionary containing the extracted keywords for each target column value.