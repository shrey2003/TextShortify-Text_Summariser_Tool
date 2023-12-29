import os
import urllib.request as request
import zipfile
import pandas as pd
import json
from pathlib import Path
from TextShortify.logging import logger
from TextShortify.utils.common import get_size
from TextShortify.entity import DataIngestionConfig

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



    def read_jsonl_to_dataframe(file_path, csv_file_path):
        """
        Reads a JSONL file, converts it into a pandas DataFrame, saves it as a CSV file, and downloads it.
        
        Parameters:
        file_path (str): Path to the JSONL file to be read.
        csv_file_path (str): Path to save the CSV file.

        Returns:
        pandas.DataFrame: DataFrame containing the data from the JSONL file.
        """
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                data.append(json.loads(line))
        
        df = pd.DataFrame(data)
        
        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        
        return df
