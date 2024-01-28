import os
import pandas as pd
import pyarrow as pa
from DocQnA.config.configuration import ConfigurationManager
from DocQnA.components.model_trainer import ModelTrainer
from DocQnA.entity import ModelTrainerConfig
from DocQnA.logging import logger

logger.info("Starting model training")

# Check if model is already present in trained_model folder
model_path = "trained_model/model_name.pth"

config = ModelTrainerConfig(
            max_seq_length=2048,
            dtype=None,
            load_in_4bit=True,
            model_name="unsloth/zephyr-sft-bnb-4bit",
            r=16,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_alpha=32,
            lora_dropout=0,
            bias="none",
            use_gradient_checkpointing=True,
            random_state=3407
        )
model_trainer = ModelTrainer(config=config)
    
