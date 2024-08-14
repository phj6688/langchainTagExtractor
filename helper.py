import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = ['english', 'deutsch', 'french']

class Config(BaseModel):
    n_tags: int
    llm: Dict[str, Any]
    template: str
    base_dir: str
    parallel_processing: Dict[str, Any] = Field(default_factory=lambda: {"enabled": False, "method": "thread", "workers": 4})

    @classmethod
    def load_config(cls, file_path: str) -> 'Config':
        """Loads configuration data from a YAML file into a Config instance."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            logger.info("Configuration loaded successfully.")
            return cls(**config_data)
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML config: {e}")
            raise
        except FileNotFoundError as e:
            logger.error(f"Configuration file not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

class ArticleBodyInfo(BaseModel):
    sentiment: str = Field(..., enum=['happy', 'neutral', 'sad'], description="Sentiment of the Article")
    language: str = Field(..., enum=SUPPORTED_LANGUAGES, description="Language of the Article")
    tags: List[str] = Field(..., description="Tags extracted from the Article")
    summary: str = Field(..., description="Summary of the Article")