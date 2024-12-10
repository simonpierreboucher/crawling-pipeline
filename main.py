# main.py
import argparse
import logging
import sys
import os

from crawler import WebCrawler
from config import (
    START_URL,
    MAX_DEPTH,
    USE_PLAYWRIGHT,
    DOWNLOAD_PDF,
    DOWNLOAD_DOC,
    DOWNLOAD_IMAGE,
    DOWNLOAD_OTHER,
    LLM_PROVIDER,
    OPENAI_API_KEYS,
    MAX_TOKENS,
    MAX_URLS,
    CRAWLER_OUTPUT_DIR,
    CHECKPOINT_FILE,
    VERBOSE
)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Exécuter le Web Crawler avec des options personnalisées.')

    parser.add_argument('--start-url', type=str, help='URL de départ pour le crawl.')
    parser.add_argument('--max-depth', type=int, help='Profondeur maximale du crawl.')
    parser.add_argument('--use-playwright', action='store_true', help='Utiliser Playwright pour les pages JavaScript.')
    parser.add_argument('--no-playwright', dest='use_playwright', action='store_false', help='Ne pas utiliser Playwright.')
    parser.add_argument('--download-pdf', action='store_true', help='Télécharger les fichiers PDF.')
    parser.add_argument('--no-download-pdf', dest='download_pdf', action='store_false', help='Ne pas télécharger les fichiers PDF.')
    parser.add_argument('--download-doc', action='store_true', help='Télécharger les documents.')
    parser.add_argument('--no-download-doc', dest='download_doc', action='store_false', help='Ne pas télécharger les documents.')
    parser.add_argument('--download-image', action='store_true', help='Télécharger les images.')
    parser.add_argument('--no-download-image', dest='download_image', action='store_false', help='Ne pas télécharger les images.')
    parser.add_argument('--download-other', action='store_true', help='Télécharger les autres types de fichiers.')
    parser.add_argument('--no-download-other', dest='download_other', action='store_false', help='Ne pas télécharger les autres types de fichiers.')
    parser.add_argument('--llm-provider', type=str, help='Fournisseur LLM à utiliser.')
    parser.add_argument('--openai-api-keys', nargs='*', help='Liste des clés API OpenAI.')
    parser.add_argument('--max-tokens', type=int, help='Nombre maximum de tokens par requête.')
    parser.add_argument('--max-urls', type=int, help='Nombre maximum d\'URLs à crawler.')
    parser.add_argument('--crawler-output-dir', type=str, help='Répertoire de sortie pour le crawler.')
    parser.add_argument('--checkpoint-file', type=str, help='Fichier de checkpoint.')
    parser.add_argument('--verbose', action='store_true', help='Activer les logs détaillés.')

    return parser.parse_args()

def setup_logging(verbose: bool):
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    args = parse_arguments()
    setup_logging(args.verbose or VERBOSE)

    # Préparer les arguments pour le crawler en donnant priorité aux arguments de la ligne de commande
    crawler_kwargs = {
        'start_url': args.start_url if args.start_url else START_URL,
        'max_depth': args.max_depth if args.max_depth else MAX_DEPTH,
        'use_playwright': args.use_playwright if 'use_playwright' in args else USE_PLAYWRIGHT,
        'download_pdf': args.download_pdf if 'download_pdf' in args else DOWNLOAD_PDF,
        'download_doc': args.download_doc if 'download_doc' in args else DOWNLOAD_DOC,
        'download_image': args.download_image if 'download_image' in args else DOWNLOAD_IMAGE,
        'download_other': args.download_other if 'download_other' in args else DOWNLOAD_OTHER,
        'llm_provider': args.llm_provider if args.llm_provider else LLM_PROVIDER,
        'api_keys': args.openai_api_keys if args.openai_api_keys else OPENAI_API_KEYS,
        'max_tokens_per_request': args.max_tokens if args.max_tokens else MAX_TOKENS,
        'max_urls': args.max_urls if args.max_urls else MAX_URLS,
        'base_dir': args.crawler_output_dir if args.crawler_output_dir else CRAWLER_OUTPUT_DIR
    }

    crawler = WebCrawler(**crawler_kwargs)

    # Si un fichier de checkpoint personnalisé est fourni
    if args.checkpoint_file:
        crawler.CHECKPOINT_FILE = args.checkpoint_file

    # Vérifier si Playwright est activé mais non installé
    if crawler.use_playwright:
        try:
            import playwright
        except ImportError:
            logging.error("Playwright est activé mais n'est pas installé. Veuillez installer Playwright en exécutant `pip install playwright` et `playwright install`.")
            sys.exit(1)

    crawler.crawl()

if __name__ == '__main__':
    main()
