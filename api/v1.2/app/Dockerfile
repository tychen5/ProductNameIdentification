#based on ncvr.io
FROM nvcr.io/nvidia/pytorch:22.09-py3
#install script
RUN pip install transformers[sentencepiece]==4.22.2 pandas==1.4.4 numpy==1.22.2 re==2.2.1 rapidfuzz==2.11.1 tableau-api-lib openpyxl inflect tqdm
# RUN python ./api/construct_dict1.py
# RUN python ./api/construct_dict2.py
# RUN python ./api/construct_dict3.py
RUN python ./api/install_models.py