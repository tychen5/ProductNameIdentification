# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names from user-generated text, such as Reddit posts. The script processes the input text, cleans it, and then calculates a score for each keyword in the text. Based on these scores, the script identifies the most relevant product names and returns them in a structured format.

### Features

- Text cleansing and preprocessing
- Keyword scoring using RapidFuzz library
- Product name extraction based on keyword scores
- Merging and combining store names using difflib library

### Functions

1. `easy_cleansing_doc(doc)`: Performs basic text cleansing on the input document.
2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given keyword in the Reddit text.
3. `clean_productline(pl_set)`: Cleans the product line set by removing 'others' and sorting the remaining items.
4. `merge(l, r)`: Merges two lists using the difflib library.
5. `combine_store_names(sn_li)`: Combines store names using the `merge()` function and the difflib library.
6. `merge_diff_sn(li_str)`: Uses diff score to combine names.
7. `chk_li_empty(li)`: Checks if a list is empty and returns a list containing 'others' if it is.
8. `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.95)`: Gets the product name from the Reddit document.
9. `product_name_inference_inhouse(input_post)`: Performs product name inference on the input post.

### Usage

To use the `product_name_inference.py` script, simply import the `product_name_inference_inhouse` function and provide it with an input post (a combination of post title and post body). The function will return a dictionary containing the inferred product names.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "I don't know how to buy Camera and what to pick in Camera G3-Instant"
result = product_name_inference_inhouse(input_post)
print(result)
```

### Dependencies

- pickle
- re
- html
- difflib
- RapidFuzz
- os

### Note

The script requires a pickle file (`api_tuples_data.pkl`) containing sensitive information, such as product data and stop words. Make sure to place this file in the same directory as the script.