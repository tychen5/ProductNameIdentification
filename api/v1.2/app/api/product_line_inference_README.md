# Product Line Inference

This Python script, `product_line_inference.py`, is designed to infer product lines from given text data. It utilizes various natural language processing techniques, machine learning models, and string manipulation methods to accurately identify and categorize product lines.

### Features

- Preprocessing of text data, including removal of special characters, emojis, and unnecessary punctuation.
- Utilizes a pre-trained Zero-Shot Learning (ZSL) model for text classification.
- Implements custom functions for filtering and refining model results based on predefined thresholds and dictionaries.
- Combines multiple inference results to generate a final, ordered list of product lines.

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

### Usage

1. Replace the file paths in the script with your own file paths for the following files:
   - `your_final_product_df.pkl`
   - `your_fl_mapping.pkl`
   - `your_em2_detect_df.pkl`
   - `your_envocab_stopword.pkl`
   - `your_reverse_pn2pl_di_lowercase.pkl`
   - `your_reverse_pn2pl_di.pkl`
   - `your_zslmodel.pkl`

2. Adjust the constants and variables as needed, such as thresholds and dictionaries.

3. Run the script to infer product lines from the given text data.

### Functions

- `get_model_res(title_res, thr, detect_di)`: Get model results based on threshold.
- `check_emtitle(li1, li2)`: Check if there is an intersection between two lists.
- `get_intersection(li1, li2, default_order=False)`: Get the intersection of two lists while keeping the order of the first list.
- `intersect_loop(li)`: Get the intersection of a list of lists.

### Note

The provided code snippet has been modified to remove sensitive information, unnecessary code/comments, and has been formatted according to Google style guidelines for Python. The overall logic and functionality of the script remain intact.