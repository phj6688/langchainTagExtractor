import logging
from typing import Union, List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain_core.language_models import BaseLLM
from .helper import Config, ArticleBodyInfo
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class LLMFactory:
    @staticmethod
    def create_llm(config: Config) -> BaseLLM:
        llm_config = config.llm
        if llm_config.get('openai'):
            return ChatOpenAI(model=llm_config['model'])
        return OllamaLLM(model=llm_config['model'])

class Extractor:
    def __init__(self, config: Config):
        self.config = config
        self.llm = LLMFactory.create_llm(config)
        self.parser = JsonOutputParser(pydantic_object=ArticleBodyInfo)
        self.prompt = PromptTemplate(
            template=self.config.template,
            input_variables=['text', 'n_tags'],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def extract_info(self, text: str) -> ArticleBodyInfo:
        """Extracts sentiment, language and tags from the given text."""
        logger.info("Extracting sentiment, language and tags from text...")
        try:
            chain = self.prompt | self.llm | self.parser
            output = chain.invoke({'text': text, 'n_tags': self.config.n_tags})
            return ArticleBodyInfo(**output)
        except Exception as e:
            logger.error(f"Error extracting information: {e}")
            raise

class ParallelExtractor:
    def __init__(self, config: Config):
        self.config = config
        self.extractor = Extractor(config)

    def extract_info_parallel(self, texts: List[str]) -> List[ArticleBodyInfo]:
        """Extracts information from multiple texts in parallel, maintaining input order."""
        parallel_config = self.config.parallel_processing
        method = parallel_config.get('method', 'thread')
        workers = parallel_config.get('workers', 4)

        # Initialize results list with None values
        results = [None] * len(texts)

        if method == 'thread':
            executor_class = ThreadPoolExecutor
        elif method == 'process':
            executor_class = ProcessPoolExecutor
        else:
            raise ValueError(f"Invalid parallel processing method: {method}")

        with executor_class(max_workers=workers) as executor:
            # Submit tasks with index tracking
            future_to_index = {
                executor.submit(self.extractor.extract_info, text): i 
                for i, text in enumerate(texts)
            }

            # Process results in order of completion
            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    result = future.result()
                    results[idx] = result
                except Exception as e:
                    logger.error(f"Error in parallel extraction for index {idx}: {e}")

        # Remove any None values (failed extractions)
        return [r for r in results if r is not None]

def create_extractor(config_path: str, parallel: bool = False) -> Union[Extractor, ParallelExtractor]:
    """Factory function to create an Extractor or ParallelExtractor instance."""
    config = Config.load_config(config_path)
    if parallel or config.parallel_processing.get('enabled', False):
        return ParallelExtractor(config)
    return Extractor(config)