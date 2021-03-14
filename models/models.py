import os
import pickle
from pathlib import Path


def save_model(my_model, file_name):  # ex : file_name = "trained_model.pickle"
    base_dir = '../models/'
    file_path = base_dir + file_name
    if os.path.exists(file_path):
        print("Model already exists")

    else:
        with open(file_path, "wb") as file:
            pickle.dump(my_model, file)
            print('Trained Model Saved')


def open_model(file_name):
    base_dir = 'models\\saved_trained_models'
    print(os.getcwd())
    file_path = os.path.join(base_dir, file_name)
    print('file path : {}'.format(file_path))
    if os.path.exists(file_path):
        print("Loading Trained Model")
        model = pickle.load(open(file_path, "rb"))

    else:
        print('No model with this name, check this and retry')
        model = None
    return model
