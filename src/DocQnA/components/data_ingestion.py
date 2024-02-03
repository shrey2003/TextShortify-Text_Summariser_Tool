import os
import urllib.request as request
import zipfile
import pandas as pd
import json
from pathlib import Path
from DocQnA.logging import logger
from DocQnA.utils.common import get_size
from DocQnA.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  

        
    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)



    def read_jsonl_to_dataframe(self):
        """
        Reads all JSONL files in a directory, converts them into pandas DataFrames, saves them as CSV files.
        
        Parameters:
        jsonl_dir (str): Path to the directory containing JSONL files.
        csv_dir (str): Path to save the CSV files.

        Returns:
        None
        """
        jsonl_dir = self.config.jsonl_file
        csv_dir = self.config.csv_file

        # Loop over all files in the directory
        for filename in os.listdir(jsonl_dir):
            # Check if the file is a .jsonl file
            if filename.endswith('.jsonl'):
                jsonl_file_path = os.path.join(jsonl_dir, filename)
                csv_file_path = os.path.join(csv_dir, filename.replace('.jsonl', '.csv'))

                data = []
                with open(jsonl_file_path, 'r') as file:
                    for line in file:
                        data.append(json.loads(line))
                
                df = pd.DataFrame(data)
                
                # Save the DataFrame to a CSV file
                df.to_csv(csv_file_path, index=False)

