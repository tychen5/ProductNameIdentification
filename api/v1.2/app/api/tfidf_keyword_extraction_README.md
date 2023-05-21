# TF-IDF Keyword Extraction

This Python script, `tfidf_keyword_extraction.py`, is designed to extract unique keywords from a given target column in a DataFrame using the Term Frequency-Inverse Document Frequency (TF-IDF) algorithm. The script is useful for text analysis and natural language processing tasks, where identifying the most important words in a corpus is essential.

### Functionality

The main function in this script is `construct_keywords(level_targetcolname_doc, target_col_name)`, which takes in a DataFrame and a target column name as input arguments and returns a dictionary containing the unique keywords for each entry in the target column.

#### Input

- `level_targetcolname_doc` (DataFrame): The input DataFrame containing the text data.
- `target_col_name` (str): The name of the target column in the DataFrame.

#### Output

- `dict`: A dictionary with keys as the target column's unique entries (level's name) and values as lists of strings representing the extracted keywords.

### Usage

1. Import the required libraries and the `construct_keywords` function from the `tfidf_keyword_extraction.py` script.
2. Prepare your input DataFrame with the text data and the target column name.
3. Call the `construct_keywords` function with the input DataFrame and target column name as arguments.
4. The function will return a dictionary containing the unique keywords for each entry in the target column.

### Example

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tfidf_keyword_extraction import construct_keywords

# Prepare your input DataFrame
data = {'first_level': ['A', 'B', 'C'],
        'doc': ['This is a sample document A.',
                'This is another sample document B.',
                'This is the third sample document C.']}
df = pd.DataFrame(data)

# Call the construct_keywords function
keywords_dict = construct_keywords(df, 'first_level')

# Output
print(keywords_dict)
# {'A': ['document', 'sample', 'a'],
#  'B': ['another', 'document', 'sample'],
#  'C': ['document', 'sample', 'third']}
```

### Dependencies

- pandas
- numpy
- itertools
- string
- sklearn (specifically, TfidfVectorizer from sklearn.feature_extraction.text)

### Note

Please ensure to replace the placeholders (e.g., "your_data_here") in the script with the actual data or variables you need to use.