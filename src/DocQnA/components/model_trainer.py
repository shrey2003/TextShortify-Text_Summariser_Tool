from DocQnA.logging import logger
from transformers import AutoTokenizer
from datasets import Dataset
from DocQnA.entity import ModelTrainerConfig
from transformers import TrainingArguments
import torch
from unsloth import FastLanguageModel
from trl import SFTTrainer

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        dataset = Dataset.from_json(self.config.data_path)
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=self.config.model_name,
            max_seq_length=self.config.max_seq_length,
            dtype=self.config.dtype,
            load_in_4bit=self.config.load_in_4bit
        )

        model = FastLanguageModel.get_peft_model(
            model,
            r=self.config.r,
            target_modules=self.config.target_modules,
            lora_alpha=self.config.lora_alpha,
            lora_dropout=self.config.lora_dropout,
            bias=self.config.bias,
            use_gradient_checkpointing=self.config.use_gradient_checkpointing,
            random_state=self.config.random_state,
            max_seq_length=self.config.max_seq_length
        )

        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            dataset_text_field="text",
            max_seq_length=self.config.max_seq_length,
            args=TrainingArguments(
                per_device_train_batch_size=32,
                gradient_accumulation_steps=1,
                warmup_steps=5,
                max_steps=50,
                learning_rate=2e-4,
                fp16=not torch.cuda.is_bf16_supported(),
                bf16=torch.cuda.is_bf16_supported(),
                logging_steps=2,
                optim="adamw_8bit",
                weight_decay=0.01,
                lr_scheduler_type="linear",
                seed=self.config.random_state,
                output_dir="outputs"
            )
        )

        trainer_stats = trainer.train()