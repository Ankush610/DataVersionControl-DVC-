import pandas as pd 
import numpy as np
import logging
import os
import warnings
warnings.filterwarnings("ignore")

log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('data_preprocessing')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'data_preprocessing.log'))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def preprocess_data(df):
    """
    Preprocess the data by removing duplicates and handling missing values.
    """
    # Remove duplicates
    try:
        initial_shape = df.shape
        df = df.drop_duplicates()
        final_shape = df.shape
        logger.info(f"Removed {initial_shape[0] - final_shape[0]} duplicates.")
    except Exception as e:
        logger.error(f"Error removing duplicates: {e}")


    # Handle missing values
    try:
        df['age'] = df['age'].ffill() # forward fill
        df['bmi'] = df['bmi'].fillna(df['bmi'].mean()) # mean fill
        df['region'] = df['region'].fillna(df['region'].mode()[0]) # mode fill for categorical
        df['charges'] = df['charges'].fillna(df['charges'].mean()) # mean fill
        logger.info("Missing values handled successfully.")
    
    except Exception as e:
        logger.error(f"Error handling missing values: {e}")

    # Convert categorical variables to numerical
    try:
        df['gender'] = df['gender'].astype('category').cat.codes
        df['smoker'] = df['smoker'].astype('category').cat.codes
        df = pd.get_dummies(df, columns=['region'], drop_first=True,dtype=np.int16) # one hot encoding for region
        df['insuranceclaim'] = df['insuranceclaim'].astype('category').cat.codes
        logger.info("Categorical variables converted to numerical successfully.")
    except Exception as e:  
        logger.error(f"Error converting categorical variables: {e}")
    
    # remove outliers
    try:
        for i in range(6):
            for i in ['age','bmi','charges']:
                    Q1 = df[i].quantile(0.25)
                    Q3 = df[i].quantile(0.75)
                    IQR = Q3 - Q1
                    df = df[df[i] <= (Q3+(1.5*IQR))]
                    df = df[df[i] >= (Q1-(1.5*IQR))]
                        
            df = df.reset_index(drop=True)
        logger.info("Outliers removed successfully.")
    except Exception as e:
        logger.error(f"Error removing outliers: {e}")

    return df


if __name__ == "__main__":

    try:
        #read the data
        df = pd.read_csv('./data/original_data.csv')
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")

    try:
        df = preprocess_data(df)
        df.to_csv('./data/preprocessed_data.csv', index=False)
        logger.info("Data preprocessing completed successfully.")
    except Exception as e:
        logger.error(f"Error during data preprocessing: {e}")