
s=str(input("""Which of the following tasks you want to carry out?
            1. Do you want to train the model? [Write 'train' for this option]
            2. Do you want to view web interface for the Doc QnA chatbot? [Write 'web' for this option]\n"""))
if s=="train":
   from DocQnA.pipeline.stage_1_data_ingestion import DataIngestionTrainingPipeline
   from DocQnA.pipeline.stage_2_data_transformation import DataTransformationTrainingPipeline
   from DocQnA.pipeline.stage_3_model_trainer import model_trainer
   from DocQnA.logging import logger
   import subprocess
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
elif s=="web":
    import subprocess
    subprocess.run(['python', 'app.py'])
    

