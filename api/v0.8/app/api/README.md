# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names from user-generated text, such as Reddit posts. The script processes the input text, cleans it, and then calculates a score for each keyword in the text. Based on these scores, the script identifies the most relevant product names and returns them in a structured format.

### Key Functions

1. `easy_cleansing_doc(doc)`: Performs basic text cleansing on the input document, such as unescaping HTML characters, replacing newlines and tabs with spaces, and removing punctuation.

2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given keyword in the Reddit text using the `rapidfuzz` library.

3. `clean_productline(pl_set)`: Cleans the product line set by removing the 'others' element and sorting the set.

4. `merge(l, r)`: Merges two lists using the `difflib` library.

5. `combine_store_names(sn_li)`: Combines store names using the `merge()` function and the `difflib` library.

6. `merge_diff_sn(li_str)`: Merges store names using the `difflib` library and the ratio of the sequences.

7. `chk_li_empty(li)`: Checks if a list is empty and returns a list with the 'others' element if it is.

8. `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.78)`: Gets the product name document from the Reddit document.

9. `product_name_inference_inhouse(input_post)`: Performs product name inference on the input post.

### Usage

To use the `product_name_inference.py` script, simply import the `product_name_inference_inhouse` function and pass in the input text as a string. The function will return a dictionary containing the inferred product names.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "Protect 2.1.2 crashing"
result = product_name_inference_inhouse(input_post)
print(result)
```

### Dependencies

- `pickle`
- `re`
- `html`
- `difflib`
- `rapidfuzz`
- `os`

### Data

The script uses a pickle file (`api_tuples_data.pkl`) containing sensitive information, such as product data, stop words, and English vocabulary. This file is loaded at the beginning of the script and used throughout the various functions.