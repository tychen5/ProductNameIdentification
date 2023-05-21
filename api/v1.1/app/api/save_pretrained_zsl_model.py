# This script saves a pre-trained zero-shot classification model to a pickle file
# Note: every time the Docker container changes CPU cores or uses CPU/GPU, this script needs to be re-run

import os
import pickle

from transformers import pipeline

# Define the path to the data directory
data_path = '/path/to/your/data/directory/'

# Initialize the zero-shot classification pipeline with a pre-trained model
classifier = pipeline(
    "zero-shot-classification",
    model="enter_your_pretrained_model_name_here",
    num_workers=1,
    device=0
)

# Save the classifier object to a pickle file
with open(os.path.join(data_path, 'zslmodel.pkl'), 'wb') as f:
    pickle.dump(classifier, f)