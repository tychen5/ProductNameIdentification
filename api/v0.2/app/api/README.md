# Product Name Inference

This Python script, `product_name_inference.py`, is designed to infer product names from user-generated text, such as forum posts or comments. The script processes the input text, cleans it, and then calculates a score based on the presence of certain keywords. It then returns the inferred product names along with their associated categories.

### Features

- Cleansing of input text
- Calculation of document scores based on keyword presence
- Merging and combining store names using SequenceMatcher
- Inference of product names and categories from input text

### Functions

1. `easy_cleansing_doc(doc)`: Cleans the input document by replacing newlines with spaces, converting to lowercase, and removing punctuation.
2. `calc_doc_score(sent_kw, reddit_text)`: Calculates the score of a document based on the presence of certain keywords.
3. `clean_productline(pl_set)`: Cleans the product line by removing 'others' and sorting the set.
4. `merge(l, r)`: Merges two strings using SequenceMatcher.
5. `combine_store_names(sn_li)`: Combines store names using SequenceMatcher and merge.
6. `merge_diff_sn(li_str)`: Uses diff score to combine names.
7. `chk_li_empty(li)`: Checks if a list is empty and returns 'others' if it is.
8. `get_product_name_doc(reddit_doc, product_df)`: Gets the product name from a document using the product dataframe.
9. `product_name_inference_inhouse(input_post)`: Infers the product name from a post.

### Usage

To use the `product_name_inference.py` script, simply import it and call the `product_name_inference_inhouse(input_post)` function with your input text as the argument. The function will return a dictionary containing the inferred product names and their associated categories.

```python
from product_name_inference import product_name_inference_inhouse

input_post = "What's required for port isolation? I've read docs and even opened a support case, but I'm still not 100% sure what is required to use the port isolation functionality. I need to isolate wired hosts from one another. The number of hosts will be well over 100, so creating a VLAN per host is not ideal.  Port isolation offers the functionality I'm looking for and I do realize it's isolation per switch - not network wide. Support referenced the link below and at first stated CloudKey or UDM. My follow to them resulted in UDM, but you don't need a Pro switch.  Hence my confusion. https://help.ui.com/hc/en-us/articles/115000166827-UniFi-Guest-Portal-and-Hotspot-System My question is what hardware is actually needed to do this?  Do I need the Pro series switches? Do I need a UDM?  I currently only have a CloudKey, AC AP, and a Pro 24 port in place.  I leverage Sonicwall as my firewall."

result = product_name_inference_inhouse(input_post)
print(result)
```

### Dependencies

- `pickle`
- `re`
- `html`
- `difflib`
- `os`