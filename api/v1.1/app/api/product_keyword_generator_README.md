# Product Keyword Generator

This Python script, `product_keyword_generator.py`, is designed to generate keywords for product categories based on their tags and store names. The script processes multiple CSV files containing product information and uses the Term Frequency-Inverse Document Frequency (TF-IDF) algorithm to extract relevant keywords for each product category.

### Input Data

The script requires the following input data files:

1. `Ubiquiti_Support_Zendesk_Fields_Historic_Problem_Device_Model.csv`
2. `Ubiquiti_Support_Zendesk_Fields_Current_Problem_Device_Model_in_ZD.csv`
3. `Ubiquiti_Support_Zendesk_Fields_Changes_for_UniFi_devices.csv`
4. `Product_SKU_and_NAME.csv`

These files should be placed in the specified `data_path` directory.

### Data Preprocessing

The script preprocesses the input data by performing the following steps:

1. Cleans and renames the columns in the input data.
2. Removes rows with invalid or missing values.
3. Cleans the text in the 'sku' and 'tag' columns by removing unnecessary characters and words.

### Keyword Generation

The script generates keywords for each product category using the following steps:

1. Constructs a corpus of documents for each product category based on their tags and store names.
2. Applies the TF-IDF algorithm to the corpus to extract relevant keywords for each product category.
3. Stores the generated keywords in a dictionary with the product category as the key.

### Output

The script outputs a dictionary containing the generated keywords for each product category. The dictionary has the following structure:

```
{
    'product_category_1': ['keyword_1', 'keyword_2', ...],
    'product_category_2': ['keyword_1', 'keyword_2', ...],
    ...
}
```

### Usage

To use the script, simply update the `data_path` variable with the correct path to your data files and run the script. The generated keywords will be stored in the `first_level_tagsku_keword_di` and `first_level_storename_keyword_di` dictionaries.

### Dependencies

The script requires the following Python libraries:

- pandas
- numpy
- scikit-learn
- itertools
- string
- inflect
- re

Make sure to install these libraries before running the script.