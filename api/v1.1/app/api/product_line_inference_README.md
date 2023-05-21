# Product Line Inference

This Python script, `product_line_inference.py`, is designed to infer product lines from given text data. It processes and analyzes text data from titles and selftexts, and then classifies them into appropriate product lines. The script also takes into account user tags for improved classification accuracy.

### Dependencies

- pandas
- pickle
- html
- string
- re
- inflect
- rapidfuzz
- gc
- torch
- os
- warnings
- transformers
- tqdm

### Data Files

The script requires several data files to function properly. Please replace the file paths in the script with your own file paths for the following data files:

- final_product_df
- fl_convert_dict
- new_em_df
- en_vocabulary_and_stop_words
- detect_di_title
- detect_di_selftext
- classifier

### Constants

The script uses several constants to fine-tune its functionality. These constants include:

- bad_puncli
- need_filtered_puncset
- need_filtered_puncset_model
- title_model_lossethr
- title_model_strictthr
- selftext_model_lossethr
- selftext_model_strictthr
- default_order
- bad_protect_name_di
- need_filtered_puncset
- sku_postfix
- emoji_pattern
- pl_si
- fmthr_di
- fmthr_dict

### Functions

The script contains several functions to process and analyze the text data:

- `get_model_res()`: Get model results based on threshold.
- `check_emtitle()`: Check if there exists an intersection between two lists.
- `get_intersection()`: Get the intersection of two lists while maintaining the order of the first list.
- `intersect_loop()`: Get the intersection of a list of lists.
- `title_res()`: Process and analyze title data.
- `selftext_res()`: Process and analyze selftext data.
- `combine_output()`: Combine the output of title and selftext analysis.
- `product_name_inference_inhouse()`: Main function to infer product lines from given text data.

### Usage

To use the script, simply import the `product_name_inference_inhouse()` function and provide it with the required input data:

```python
from product_line_inference import product_name_inference_inhouse

# Replace with your own input data
title_list = [...]
selftext_list = [...]
user_tag_list_list = [...]

result = product_name_inference_inhouse(title_list, selftext_list, user_tag_list_list)
```

The `result` variable will contain the inferred product lines for the given input data.