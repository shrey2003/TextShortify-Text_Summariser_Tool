from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path
    jsonl_file: Path
    csv_file: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    max_seq_length: int
    dtype: str
    load_in_4bit: bool
    model_name: str
    r: int
    target_modules: list
    lora_alpha: int
    lora_dropout: int
    bias: str
    use_gradient_checkpointing: bool
    random_state: int