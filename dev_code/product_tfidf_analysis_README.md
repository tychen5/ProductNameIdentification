# Product TF-IDF Analysis

This Python script, `product_tfidf_analysis.py`, is designed to analyze product data and Reddit posts to generate relevant keywords and preprocess the text data. The script uses various libraries such as pandas, numpy, pymongo, itertools, re, string, html, inflect, pandarallel, difflib, and rapidfuzz.

### Features

1. Load product data from a pickle file and preprocess it.
2. Connect to a MongoDB database to fetch Reddit data and convert it into a DataFrame.
3. Preprocess Reddit data by cleansing the text and combining the title and selftext.
4. Apply text cleansing and preprocessing functions to the product and Reddit data.
5. Merge similar store names using difflib's SequenceMatcher.
6. Filter the final product DataFrame based on specific keywords.

### Usage

To use this script, you need to have Python 3.x installed along with the required libraries mentioned above. Replace the placeholders (e.g., 'your_host', 'your_username', 'your_password', etc.) with your actual values. Also, replace the `need_filtered_puncset`, `stop_words`, and `en_vocabulary` variables with your actual data.

Run the script using the following command:

```bash
python product_tfidf_analysis.py
```

### Functions

- `concate_doc()`: Concatenates the first, second, and third level attributes with the store name.
- `mongo_to_df(filter_day=7)`: Connects to a MongoDB database, fetches Reddit data, and converts it into a DataFrame.
- `concate_all_words(col_li)`: Concatenates all words from the given list of columns.
- `easy_cleansing_doc(doc)`: Cleanses the input document by removing unnecessary characters and splitting it into words.
- `reddit_cleansing(title, selftext)`: Cleanses Reddit data using the data cleansing function mentioned above and combines the title and selftext.
- `merge_diff_sn(li_str)`: Uses diff score to combine names.
- `find_word(s)`: Checks if the given word is present in the string.

### Example

An example usage of the script is provided within the code itself. Replace the example data with your actual data to see the results.

### Note

The `combine_store_names` function is missing in the provided code, so you will need to add it to make the `merge_diff_sn` function work correctly.