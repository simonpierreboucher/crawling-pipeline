# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration par défaut
START_URL = os.getenv('START_URL', 'https://example.com')
MAX_DEPTH = int(os.getenv('MAX_DEPTH', 3))
USE_PLAYWRIGHT = os.getenv('USE_PLAYWRIGHT', 'False').lower() in ['true', '1', 't']
DOWNLOAD_PDF = os.getenv('DOWNLOAD_PDF', 'False').lower() in ['true', '1', 't']
DOWNLOAD_DOC = os.getenv('DOWNLOAD_DOC', 'False').lower() in ['true', '1', 't']
DOWNLOAD_IMAGE = os.getenv('DOWNLOAD_IMAGE', 'False').lower() in ['true', '1', 't']
DOWNLOAD_OTHER = os.getenv('DOWNLOAD_OTHER', 'False').lower() in ['true', '1', 't']
LLM_PROVIDER = os.getenv('LLM_PROVIDER', None)
OPENAI_API_KEYS = os.getenv('OPENAI_API_KEYS', '').split() if os.getenv('OPENAI_API_KEYS') else []
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
MAX_URLS = int(os.getenv('MAX_URLS', 1000)) if os.getenv('MAX_URLS') else None
CRAWLER_OUTPUT_DIR = os.getenv('CRAWLER_OUTPUT_DIR', 'crawler_output')
CHECKPOINT_FILE = os.getenv('CHECKPOINT_FILE', 'checkpoint.json')
VERBOSE = os.getenv('VERBOSE', 'False').lower() in ['true', '1', 't']
