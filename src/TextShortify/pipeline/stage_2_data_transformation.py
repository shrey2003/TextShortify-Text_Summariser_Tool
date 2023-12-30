import os
import pandas as pd
import pyarrow as pa
from TextShortify.config.configuration import ConfigurationManager
from TextShortify.components.data_transformation import DataTransformation
from TextShortify.logging import logger


class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        train_df= pd.read_csv(os.path.join(data_transformation_config.data_path, "train.csv"))
        test_df= pd.read_csv(os.path.join(data_transformation_config.data_path, "test.csv"))
        # Convert pandas DataFrame to Arrow Table
        train_table = pa.Table.from_pandas(train_df)
        test_table = pa.Table.from_pandas(test_df)

        # Pass Arrow Tables to DataTransformation
        data_transformation_train = DataTransformation(config=data_transformation_config, data=train_table)
        data_transformation_test = DataTransformation(config=data_transformation_config, data=test_table)
        train_dataset=data_transformation_train.save_to_disk(os.path.join(data_transformation_config.root_dir, 'train_data'))
        test_dataset=data_transformation_test.save_to_disk(os.path.join(data_transformation_config.root_dir, 'test_data'))
        