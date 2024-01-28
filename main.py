from TextShortify.pipeline.stage_1_data_ingestion import DataIngestionTrainingPipeline
from TextShortify.pipeline.stage_2_data_transformation import DataTransformationTrainingPipeline
from DocQnA.pipeline.stage_3_model_trainer import model_trainer
from TextShortify.logging import logger
import os

STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Data Transformation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_transformation = DataTransformationTrainingPipeline()
   data_transformation.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Model Training stage"
model_path = "trained_model/model_name.pth"

try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   if not os.path.exists(model_path):
      model_trainer.train()
   else:
      logger.info("Model already exists in trained_model folder")
   
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        raise e

