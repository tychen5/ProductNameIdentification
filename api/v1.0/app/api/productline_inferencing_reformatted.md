product_line_inference.py

# README.md

## Product Line Inference

This Python script, `product_line_inference.py`, is designed to infer product names and categories based on input data such as titles, selftexts, and user tags. The script utilizes various natural language processing techniques, string matching algorithms, and machine learning models to achieve accurate product line inference.

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

### Key Functions

1. `title_res()`: Determines the final title result list based on various input lists, such as strict and loose title results, selftext results, and user tags.

2. `product_name_inference_inhouse()`: Infers product names based on input title, selftext, and user tag lists.

### Usage

To use this script, you need to replace the placeholders in the file paths with the actual file names or paths you want to use. For example, replace `'enter_your_final_product_df_file.pkl'` with the actual file path of your final product DataFrame.

After setting up the file paths, you can call the `product_name_inference_inhouse()` function with the input title list, selftext list, and user tag list to infer product names and categories.

Example:

```python
input_title_list = ["Protect 2.1.2 crashing", 'what should I replace my USG with, UDM, UDMpro or UDR?']
input_selftext_list = ["I don't know how to buy Camera and what to pick in Camera G3-Instant", "What's required for port isolation? ..."]
input_productline_ori = [[], ['unifi', 'unifi-routing-switching', 'unifi-wireless']]

product_name_inference_inhouse(input_title_list, input_selftext_list, input_productline_ori)
```

### Note

This script has been modified to remove sensitive information and formatted according to Google style guidelines for Python. Make sure to replace the placeholders with the actual file names or paths you want to use before running the script.