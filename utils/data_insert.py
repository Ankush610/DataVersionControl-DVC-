import pandas as pd 
import logging 
import os 

log_dir = './logs'

os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger('data_insert')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'data_insert.log'))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

try:
    df = pd.read_csv('./insurance_Claim.csv')    
    df.to_csv('./data/original_data.csv', index=False)
    logger.info("Data inserted successfully.")
except Exception as e:
    logger.error(f"Error inserting data: {e}")
