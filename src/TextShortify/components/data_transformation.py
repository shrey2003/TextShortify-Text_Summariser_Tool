from TextShortify.logging import logger
from transformers import AutoTokenizer
from datasets import Dataset
from TextShortify.entity import DataTransformationConfig

class DataTransformation(Dataset):
    def __init__(self,data,config: DataTransformationConfig):
        super().__init__(data)
        self.config = config
        self.tokenizer= AutoTokenizer.from_pretrained(config.tokenizer_name)
        
    def __len__(self):
        return len(self.data)
    
    def convert_examples_to_features(self,idx):
        item = self.data.iloc[idx]  # Get the row at the specified index
        judgement = item['judgement'] # Extract dialogue from the row
        summary = item['summary']   # Extract summary from the row

        # Encode the dialogue as input data for the model
        source = self.tokenizer.encode_plus(
            judgement, 
            max_length=2048, 
            padding='max_length', 
            truncation=True
        )

        # Encode the summary as target data for the model
        target = self.tokenizer.encode_plus(
            summary, 
            max_length=512, 
            padding='max_length', 
            truncation=True
        )

        # Return a dictionary containing input_ids, attention_mask, labels, and the original summary text
        return {
            'input_ids': source['input_ids'].flatten(),
            'attention_mask': source['attention_mask'].flatten(),
            'labels': target['input_ids'].flatten(),
            'summary': summary 
        }