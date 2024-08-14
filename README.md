# LangChain Tag Extractor

## Overview
LangChain Tag Extractor is a Python-based tool designed to extract relevant information from news articles. It uses LLMs to analyze text and extract tags, determine sentiment, identify the language, and provide a concise summary.

## Features
- Extract tags from news articles
- Determine article sentiment (happy, neutral, sad)
- Identify article language
- Generate concise summaries
- Support for parallel processing (multi-threading and multi-processing)
- Configurable via YAML file

## Requirements
- Python 3.x
- Dependencies: langchain, pydantic, PyYAML, python-dotenv

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key in a `.env` file

## Configuration
Adjust the `config.yaml` file to customize:
- Number of tags to extract
- Language model settings
- Parallel processing options
- Prompt template (not recommended to change)

## Usage
```python
from langchainTagExtractor.extractor import create_extractor

config_path = "path/to/config.yaml"
extractor = create_extractor(config_path, parallel=True)

# Single extraction
result = extractor.extract_info("Article text here")

# Parallel extraction
articles = ["Article 1", "Article 2", "Article 3"]
results = extractor.extract_info_parallel(articles)
```
## Project Structure

- `extractor.py`: Main logic for text extraction
- `helper.py`: Utility classes and functions
- `config.yaml`: Configuration file

## Parallel Processing
The tool supports both multi-threading and multi-processing for parallel extraction. Configure in `config.yaml`:

```yaml
parallel_processing:
  enabled: True
  method: process  # or 'thread'
  workers: 4
```
