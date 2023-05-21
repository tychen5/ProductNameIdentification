# This script is used to create a zero-shot classification pipeline using the transformers library.
# It saves the trained model as a pickle file in the specified data path.
# The model used is "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli".
# The number of workers used is equal to the number of CPU cores available.
# The device used is the first GPU available (if any), otherwise the CPU is used.

# Import necessary libraries
from transformers import pipeline
import pickle
import os

# Define the data path where the trained model will be saved
data_path = './data/'

# Create a zero-shot classification pipeline using the specified model, number of workers, and device
classifier = pipeline("zero-shot-classification",
                        model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli",
                        num_workers=os.cpu_count(),
                        device=0)

# Save the trained model as a pickle file in the specified data path
pickle.dump(obj=classifier, file=open(data_path+'zslmodel.pkl', 'wb'))