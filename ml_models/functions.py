import os
import pickle


def save_model(my_model, file_name):
    """
        Saved my_model in ml_models/saved_trained_models/file_name
    Parameters
    ----------
    my_model : object
        Models to saved.
    file_name : str
        Named of the model used in the path

    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_folder = os.path.join(BASE_DIR, os.path.basename('ml_models'))
    models_folder = os.path.join(models_folder, os.path.basename('saved_trained_models'))
    file_path = os.path.join(models_folder, os.path.basename(file_name))
    if os.path.exists(file_path):
        print("Model named '{}' already exists".format(file_name))

    else:
        with open(file_path, "wb") as file:
            pickle.dump(my_model, file)
            print('Trained Model Saved : {}'.format(file_name))

    return None


def open_model(file_name):
    """
        Open the model saved in ml_models/saved_trained_models/file_name
    Parameters
    ----------
    file_name : str
        Named of the model used in the path

    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_folder = os.path.join(BASE_DIR, os.path.basename('ml_models'))
    models_folder = os.path.join(models_folder, os.path.basename('saved_trained_models'))
    file_path = os.path.join(models_folder, os.path.basename(file_name))

    if os.path.exists(file_path):
        print("Loading Trained Model : {}".format(file_name))
        model = pickle.load(open(file_path, "rb"))

    else:
        print("No model named '{}', check this and retry".format(file_name))
        model = None
    return model
