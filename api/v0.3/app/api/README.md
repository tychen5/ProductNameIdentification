# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names and their associated categories from Reddit posts. The script processes the input text, cleans it, and then calculates a score based on the similarity between the input text and a set of predefined keywords. The script then returns the product name along with its first, second, and third-level categories.

### Dependencies

- `pickle`
- `re`
- `html`
- `difflib`
- `rapidfuzz`

### Functions

1. `easy_cleansing_doc(doc)`: Performs basic text cleaning on the input document.
2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a given set of keywords against a Reddit post.
3. `clean_productline(pl_set)`: Cleans the product line set by removing 'others' and sorting the remaining items.
4. `merge(l, r)`: Merges two lists using the difflib library.
5. `combine_store_names(sn_li)`: Combines a list of store names using the merge function and the difflib library.
6. `merge_diff_sn(li_str)`: Merges a list of store names using the difflib library and a similarity threshold.
7. `chk_li_empty(li)`: Checks if a list is empty and returns a list containing 'others' if it is.
8. `get_product_name_doc(reddit_doc, product_df=final_product_df, thr=0.95)`: Gets the product name, first level, second level, and third level categories for a given Reddit post.
9. `product_name_inference_inhouse(input_post)`: Performs product name inference on a given Reddit post.

### Usage

To use the `product_name_inference.py` script, simply import it and call the `product_name_inference_inhouse(input_post)` function with the desired Reddit post as the input. The function will return a dictionary containing the inferred product name and its associated categories.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "I don't know how to buy Camera and what to pick in Camera G3-Instant"
result = product_name_inference_inhouse(input_post)

print(result)
```

The output will be a dictionary containing the product name and its associated categories:

```
{
    'first_level': ['first_level_category'],
    'second_level': ['second_level_category'],
    'third_level': ['third_level_category'],
    'product_name': ['product_name']
}
```

### Demo

A demo text is provided in the script as an example:

```python
input_post = "what should I replace my USG with, UDM, UDMpro or UDR?My USG took a crap today so need a replacement and with the USG basically end of life I am looking at the UDM, the UDMpro or UDR.. I have a basic home network with 1 switch and single AP the network is not complex with a couple of VLANs and some routing rules for an Unraid Box running plex, nextcloud etx. I am leaning towards the UDR but would like to hear some pro's /con's of each"
result = product_name_inference_inhouse(input_post)
print(result)
```