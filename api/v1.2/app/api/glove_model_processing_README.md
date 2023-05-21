# GloVe Model Processing

This Python script processes a GloVe model, filters out bad tokens, and constructs a list of unique sets from a list of lists of lists. The script also saves the processed DataFrame as a pickle file.

### Dependencies

- Python 3
- pandas
- itertools
- pickle

### Usage

1. Replace the placeholders in the code with the actual paths to your GloVe file, stop words file, data file, and save file.
2. Replace the `new_em_df` variable with your actual DataFrame variable.
3. Run the script.

### Functions

- `load_glove_model(file_path)`: Loads a GloVe model from a file and returns a list of words in the model.
- `filter_out_bad_set(ori_set, bad_set)`: Filters out bad tokens from the original set and adjusts token length.
- `construct_detect_di(lilili)`: Constructs a list of unique sets from a list of lists of lists.

### Workflow

1. Load the GloVe model using the `load_glove_model()` function.
2. Filter out bad tokens from the original set using the `filter_out_bad_set()` function.
3. Construct a list of unique sets using the `construct_detect_di()` function.
4. Save the processed DataFrame as a pickle file.

### Notes

- Make sure to include the conditions for `fl_name` values that were removed due to the response size limit.
- Replace the placeholders with your actual data and paths before running the script.