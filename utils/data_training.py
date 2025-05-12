import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import yaml     
import logging
import os
from dvclive import Live

log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('data_training')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'data_training.log'))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_params(params_path):
    try:
        with open(params_path,'r') as file:
            params = yaml.safe_load(file)
        logger.info("params loaded sucessfully!")
        return params
    except Exception as e:
        logger.error(f"Loading Params caused error {e}")


def prepare_data(data, target_column,TEST_SIZE,RANDOM_STATE,stratify):
    """
    Prepares the data for training by splitting it into features and target variables.
    """

    try:

        # Split the data into features and target variable
        X = data.drop(columns=[target_column])
        y = data[target_column]

        if stratify == True:
            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE,stratify=y)
        else:
            x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

        logger.info(f"Data split into training and testing sets with test size {TEST_SIZE} and random state {RANDOM_STATE}.")
        return x_train, x_test, y_train, y_test
    
    except Exception as e:
        logger.error(f"Error in prepare_data: {e}")


def train_model(model, x_train, y_train):
    """
    Trains the model on the training data.
    """
    try:
        model.fit(x_train, y_train)
        logger.info("Model training completed.")
        return model
    except Exception as e:
        logger.error(f"Error in train_model: {e}") 


def evaluate_model(model, x_test, y_test):
    """
    Evaluates the model on the testing data.
    """
    try:
        y_pred = model.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)

        with Live(save_dvc_exp=True) as live:
            live.log_metric('accuracy_score',accuracy)

        logger.info(f"Model evaluation completed with accuracy: {accuracy}")
        return accuracy
    except Exception as e:
        logger.error(f"Error in evaluate_model: {e}")


if __name__=='__main__':

    try:
        param_path = './params.yaml'
        params = load_params(param_path)
        df = pd.read_csv('./data/preprocessed_data.csv')
        target_column = 'insuranceclaim'
        TEST_SIZE = params['data_training']['test_size']
        RANDOM_STATE = params['data_training']['random_state']
        stratify = True
        model = RandomForestClassifier()
    except Exception as e:
        logger.error(f"Error in loading data or model: {e}")
        exit(1)

    x_train, x_test, y_train, y_test = prepare_data(df, target_column, TEST_SIZE, RANDOM_STATE, stratify)
    
    model = train_model(model, x_train, y_train)
    
    accuracy = evaluate_model(model, x_test, y_test)



    try:
        model_dir = './model'
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, 'trained_model.pkl')
        
        with open(model_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        
        logger.info(f"Model saved successfully at {model_path}.")
    except Exception as e:
        logger.error(f"Error in saving model: {e}")
    

