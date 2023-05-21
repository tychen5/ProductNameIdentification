`tfidf_keyword_extraction.py`

# README.md

## Tfidf Keyword Extraction

This Python script, `tfidf_keyword_extraction.py`, is designed to extract keywords from a given dataset using the Term Frequency-Inverse Document Frequency (TF-IDF) method. The script processes input data, constructs unique terms with their respective TF-IDF values, and generates a dictionary containing the extracted keywords.

### Features

- Utilizes the `TfidfVectorizer` from the `sklearn.feature_extraction.text` library to compute the TF-IDF values.
- Processes input data in the form of a pandas DataFrame.
- Constructs a dictionary with keys representing the target column name and values containing the list of extracted keywords.
- Filters out unnecessary punctuation from the keywords.
- Fills missing values in the first, second, and third levels of the dataset using the extracted keywords.
- Saves the final DataFrame as a pickle file.

### Usage

1. Import the `construct_keywords` function from the script.
2. Prepare your input data as a pandas DataFrame with the required columns.
3. Call the `construct_keywords` function with the input DataFrame and the target column name as arguments.
4. Process the resulting keyword dictionary as needed.

### Example

```python
import pandas as pd
from tfidf_keyword_extraction import construct_keywords

# Prepare your input data as a pandas DataFrame
input_data = pd.DataFrame()

# Call the construct_keywords function
keyword_dict = construct_keywords(input_data, 'target_column_name')

# Process the resulting keyword dictionary
print(keyword_dict)
```

### Dependencies

- Python 3.6 or higher
- pandas
- numpy
- scikit-learn
- pickle
- itertools
- string

### Note

Please ensure that you replace the dummy data and file paths in the script with your actual data and desired file paths before running the script.