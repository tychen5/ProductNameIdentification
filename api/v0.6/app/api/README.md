# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names from user-generated text, such as Reddit posts. The script processes the input text, cleans it, and then calculates a score for each keyword in the text. Based on these scores, the script identifies the most relevant product names and returns them in a structured format.

### Features

- Text cleansing and preprocessing
- Keyword scoring based on token set ratio
- Product name extraction from user-generated text
- Store name merging using difflib library
- Handling of missing or ambiguous product names

### Dependencies

- `pickle`
- `re`
- `html`
- `difflib`
- `rapidfuzz`
- `os`

### Functions

1. `easy_cleansing_doc(doc)`: Performs basic text cleansing on the input document.
2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given keyword in the Reddit text.
3. `clean_productline(pl_set)`: Cleans the product line set by removing 'others' and sorting the remaining items.
4. `merge(l, r)`: Merges two lists using the difflib library.
5. `combine_store_names(sn_li)`: Combines store names using the `merge()` function and the difflib library.
6. `merge_diff_sn(li_str)`: Merges store names using the difflib library and a similarity threshold.
7. `chk_li_empty(li)`: Checks if a list is empty and returns a list containing 'others' if it is.
8. `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.85)`: Gets the product name document from the Reddit document.
9. `product_name_inference_inhouse(input_post)`: Performs product name inference on the input post.

### Usage

To use the `product_name_inference.py` script, simply import it and call the `product_name_inference_inhouse(input_post)` function with the input text as an argument. The function will return a dictionary containing the inferred product names.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "Protect 2.1.2 crashing"
result = product_name_inference_inhouse(input_post)
print(result)
```

### Output

The output will be a dictionary containing the inferred product names, organized by first level, second level, third level, and product name.

Example output:

```python
{
    'first_level': ['others'],
    'second_level': ['others'],
    'third_level': ['others'],
    'product_name': ['unifi protect']
}
```