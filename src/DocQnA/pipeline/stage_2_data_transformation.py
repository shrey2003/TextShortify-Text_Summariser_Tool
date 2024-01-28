import os
import pandas as pd
import pyarrow as pa
from TextShortify.config.configuration import ConfigurationManager
from TextShortify.components.data_transformation import DataTransformation
from TextShortify.logging import logger

import logging

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        logging.info("Loading training and test data...")
        if data_transformation_config.data_ingestion:
            from datasets import load_dataset
            # Import the load_dataset function from the datasets library

            dataset = load_dataset("yahma/alpaca-cleaned", split="train")
            # Load the training data of the cleaned version of the Alpaca dataset from yahma

            dataset = dataset.map(DataTransformation.formatting_prompts_func, batched=True,)
            logging.info("Data transformation completed.")
        else:
            logging.info("No data available for data ingestion.")
        