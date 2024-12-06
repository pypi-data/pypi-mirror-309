import os
from dotenv import load_dotenv
from transformers import BertConfig, BertTokenizer, BertForSequenceClassification
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Default model directory
        self.MODEL_DIR = os.getenv(
            "MODEL_DIR", 
            os.path.join(os.path.dirname(__file__), "model")
        )

        # Load configuration, tokenizer, and model
        logger.info(f"Loading config from {self.MODEL_DIR}")
        self.CONFIG = BertConfig.from_pretrained(self.MODEL_DIR)
        logger.info("Config loaded successfully.")

        logger.info(f"Loading tokenizer from {self.MODEL_DIR}")
        self.TOKENIZER = BertTokenizer.from_pretrained(self.MODEL_DIR)
        logger.info("Tokenizer loaded successfully.")

        logger.info(f"Loading model from {self.MODEL_DIR}")
        self.LANGUAGE_MODEL = BertForSequenceClassification.from_pretrained(
            self.MODEL_DIR, config=self.CONFIG
        )
        logger.info("Model loaded successfully.")

    def get_model_and_tokenizer(self):
        return self.LANGUAGE_MODEL, self.TOKENIZER
