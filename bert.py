import torch
import pandas as pd
from transformers import pipeline, AutoTokenizer

transformer_model_name = 'dccuchile/bert-base-spanish-wwm-cased'
tokenizer = AutoTokenizer.from_pretrained(transformer_model_name)
transformer_models = ['bondi/bert-semaphore-prediction-w0',
                      'bondi/bert-semaphore-prediction-w2',
                      'bondi/bert-semaphore-prediction-w4',
                      'bondi/bert-semaphore-prediction-w8']
transformer_models_clean = ['bondi/bert-clean-semaphore-prediction-w0',
                            'bondi/bert-clean-semaphore-prediction-w2',
                            'bondi/bert-clean-semaphore-prediction-w4',
                            'bondi/bert-clean-semaphore-prediction-w8']

semaphore_classes = ['amarillo', 'naranja', 'rojo', 'verde']
semaphore_labels = ['LABEL_1', 'LABEL_2', 'LABEL_3', 'LABEL_0']
mapping = dict(zip(semaphore_labels, semaphore_classes))

def get_prediction_vector(text, clean_models=False):
    transformer_pipelines = []
    tokenizer_kwargs = {'padding': True, 'truncation': True, 'max_length': 512}
    if clean_models:
        for model in transformer_models_clean:
            transformer_pipelines.append(pipeline(model=model, tokenizer=tokenizer))
    else:
        for model in transformer_models:
            transformer_pipelines.append(pipeline(model=model, tokenizer=tokenizer))


    def predict(text, pipeline):
        return pipeline(text, **tokenizer_kwargs)[0]['label']


    label_dict = {'W0': None, 'W2': None, 'W4': None, 'W8': None}
    label_vector = [None] * len(transformer_pipelines)
    for i in range(len(transformer_pipelines)):
        label_vector[i] = mapping[predict(text, transformer_pipelines[i])]
    return label_vector
