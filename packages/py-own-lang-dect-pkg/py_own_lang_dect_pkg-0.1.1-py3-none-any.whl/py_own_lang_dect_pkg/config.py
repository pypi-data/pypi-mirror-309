import os
import tarfile
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
        
        # Path to the tar.gz model file (explicit path)
        self.TAR_GZ_MODEL_PATH = os.getenv(
            "TAR_GZ_MODEL_PATH", 
            os.path.join(os.path.dirname(__file__), "..", "py_own_lang_dect_pkg", "model.tar.gz")
        )
        
        # Directory to extract the model
        self.MODEL_DIR = os.getenv(
            "MODEL_DIR", 
            os.path.join(os.path.dirname(__file__), "extracted_model")
        )

        # Ensure the model is extracted
        self._ensure_model_extracted()

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

    def _ensure_model_extracted(self):
        """
        Ensure the model files are extracted from the tar.gz archive.
        """
        if not os.path.exists(self.MODEL_DIR):
            logger.info(f"Extracting model from {self.TAR_GZ_MODEL_PATH} to {self.MODEL_DIR}")
            with tarfile.open(self.TAR_GZ_MODEL_PATH, "r:gz") as tar_ref:
                tar_ref.extractall(self.MODEL_DIR)
            logger.info("Model extraction completed.")
        else:
            logger.info(f"Model directory already exists: {self.MODEL_DIR}")

    def get_model_and_tokenizer(self):
        """
        Returns the language model and tokenizer.
        """
        return self.LANGUAGE_MODEL, self.TOKENIZER
