import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import yaml
import os
import pkg_resources
from .unique_values import topics, subtopics


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = [
    "English",
    "Chinese",
    "Spanish",
    "German",
    "French",
    "Russian",
    "Portuguese",
    "Japanese",
    "Italian",
    "Turkish",
    "Polish",
    "Dutch",
    "Arabic",
    "Korean",
    "Vietnamese",
    "Farsi",
    "Ukrainian",
    "Hindi",
    "Thai",
    "Czech",
    "Romanian",
    "Swedish",
    "Hebrew",
    "Hungarian",
    "Finnish",
    "Greek",
    "Indonesian",
    "Danish",
    "Norwegian",
    "Slovak"
]
class Config(BaseModel):
    n_tags: int
    llm: Dict[str, Any]
    template: str
    parallel_processing: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": False,
              "method": "thread",
                "workers": 4
        }
    )

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


topics_list = topics
subtopics_list = subtopics


class Tags(BaseModel):
    topics: List[str] = Field(...,enum=topics_list, description="List of topics extracted from the Article")
    subtopics: List[str] = Field(..., enum=subtopics_list, description="List of subtopics extracted from the Article")

class ArticleBodyInfo(BaseModel):
    sentiment: str = Field(..., enum=['happy', 'neutral', 'sad'], description="Sentiment of the Article")
    language: str = Field(..., enum=SUPPORTED_LANGUAGES, description="Language of the Article")
    tags: Tags = Field(..., description="Tags extracted from the Article")
    summary: str = Field(..., description="Summary of the Article")

def get_default_config_path():
    """Returns the path to the default config file included with the package."""
    return pkg_resources.resource_filename('langchain_tag_extractor', 'config.yaml')