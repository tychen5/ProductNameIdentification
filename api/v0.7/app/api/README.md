# Product Name Inference

This Python script, `product_name_inference.py`, is designed to extract product names and their associated categories from a given text input, such as a Reddit post. The script performs text cleansing, calculates similarity scores between the input text and a set of predefined product names, and returns the most relevant product names along with their respective categories.

### Key Functions

1. `easy_cleansing_doc(doc)`: Performs basic text cleansing on the input document, such as unescaping HTML characters, converting to lowercase, and removing certain punctuation characters.

2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given set of keywords against a Reddit post using the RapidFuzz library.

3. `clean_productline(pl_set)`: Cleans a set of product line names by removing the 'others' category and sorting the names alphabetically.

4. `merge(l, r)`: Merges two lists of strings using the difflib library.

5. `combine_store_names(sn_li)`: Combines a list of store names using the `merge()` function and the difflib library.

6. `merge_diff_sn(li_str)`: Merges a list of store names using the difflib library and a similarity threshold.

7. `chk_li_empty(li)`: Checks if a list is empty and returns a list containing the string 'others' if it is.

8. `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.75)`: Extracts the product name, first level, second level, and third level categories from a Reddit post.

9. `product_name_inference_inhouse(input_post)`: Performs product name inference on a Reddit post.

### Usage

To use the `product_name_inference.py` script, simply import the `product_name_inference_inhouse` function and provide a text input (e.g., a Reddit post) as an argument. The function will return a dictionary containing the inferred product name and its associated categories.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "Protect 2.1.2 crashing"
result = product_name_inference_inhouse(input_post)
print(result)
```

### Dependencies

- Python 3.6 or later
- RapidFuzz library
- difflib library
- pickle library
- re library
- html library
- os library

### Data

The script relies on a pickle file (`api_tuples_data.pkl`) containing sensitive information, such as product names and categories. This file should be placed in the same directory as the script.