# Product Line Inference

This Python script, `product_line_inference.py`, is designed to predict product lines based on user-generated content such as titles and selftext. The script utilizes various data preprocessing techniques, machine learning models, and fuzzy matching to provide accurate predictions.

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

### Data Files

The script requires several data files to function properly. These files should be placed in the specified `data_path` directory. Replace the placeholders in the code with the appropriate file names:

- final_product_df.pkl
- fl_convert_dict.pkl
- new_em_df.pkl
- en_vocabulary.pkl
- stop_words.pkl
- detect_di_title.pkl
- detect_di_selftext.pkl
- classifier.pkl

### Constants and Variables

The script defines several constants and variables that are used throughout the code. These include:

- bad_puncli: Set of unwanted punctuation characters
- need_filtered_puncset: Set of punctuation characters to be filtered
- title_model_lossethr: Threshold for title model loose predictions
- title_model_strictthr: Threshold for title model strict predictions
- selftext_model_lossethr: Threshold for selftext model loose predictions
- selftext_model_strictthr: Threshold for selftext model strict predictions
- default_order: Default order of product lines
- bad_protect_name_di: Dictionary of bad product names
- sku_postfix: List of SKU postfixes
- emoji_pattern: Regular expression pattern for emojis
- pl_si: Inflect engine instance
- fmthr_di: Dictionary of fuzzy match thresholds
- fmthr_dict: Dictionary of fuzzy match thresholds (loaded directly)

### Functions

The script contains several functions that perform various tasks such as data preprocessing, model prediction, and result filtering. Some of the key functions include:

- `convert_user_tag()`: Converts user tags to a list of product lines
- `model_predict()`: Predicts product lines using a pre-trained classifier
- `get_model_res()`: Filters model results based on a threshold and label conversion dictionary
- `check_emtitle()`: Checks if there is an intersection between two lists
- `get_intersection()`: Gets the intersection of two lists while maintaining the order of the first list
- `intersect_loop()`: Gets the intersection of a list of lists

### Usage

To use the script, simply import the necessary functions and call them with the appropriate input data. For example:

```python
from product_line_inference import convert_user_tag, model_predict

user_tags = ['unifi', 'access']
converted_tags = convert_user_tag(user_tags)
title_clean = "Example title for product line prediction"
all_names = ["Product 1", "Product 2", "Product 3"]

model_results = model_predict(title_clean, all_names)
```

Make sure to replace the placeholders in the code with the appropriate file names and adjust the `data_path` variable as needed.