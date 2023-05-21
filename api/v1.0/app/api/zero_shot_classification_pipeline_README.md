# Zero-Shot Classification Pipeline

This Python script creates a zero-shot classification pipeline using the transformers library. The purpose of this script is to train a model for zero-shot classification tasks and save the trained model as a pickle file for future use.

### Model

The model used in this script is "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli". This is a pre-trained DeBERTa model fine-tuned for zero-shot classification tasks.

### Parallelism

The number of workers used in the pipeline is set to the number of CPU cores available on the system. This ensures optimal parallelism and efficient use of system resources.

### Device

The script uses the first available GPU (if any) for training the model. If no GPU is available, the CPU is used.

### Output

The trained model is saved as a pickle file in the specified data path (`./data/`). The filename of the saved model is `zslmodel.pkl`.

### Dependencies

- transformers
- pickle
- os

### Usage

To use this script, simply run the `zero_shot_classification_pipeline.py` file. The script will automatically train the model and save it as a pickle file in the specified data path.

```bash
python zero_shot_classification_pipeline.py
```

After running the script, you can load the trained model using the pickle library and use it for zero-shot classification tasks.

```python
import pickle

data_path = './data/'
classifier = pickle.load(open(data_path+'zslmodel.pkl', 'rb'))
```