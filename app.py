# app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Remplacez par une clé secrète sécurisée
socketio = SocketIO(app, cors_allowed_origins="*")

crawler_thread = None
crawler = None

def status_update_handler(event_type, data):
    socketio.emit('status_update', {'event': event_type, 'data': data})

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/start', methods=['POST'])
def start_crawl():
    global crawler_thread, crawler

    if crawler_thread and crawler_thread.is_alive():
        return jsonify({'status': 'error', 'message': 'Le crawler est déjà en cours d\'exécution.'}), 400

    # Récupérer la configuration depuis la requête
    config = request.json

    # Initialiser le crawler avec la configuration et le callback
    crawler = WebCrawler(
        start_url=config.get('start_url', START_URL),
        max_depth=int(config.get('max_depth', MAX_DEPTH)),
        use_playwright=bool(config.get('use_playwright', USE_PLAYWRIGHT)),
        download_pdf=bool(config.get('download_pdf', DOWNLOAD_PDF)),
        download_doc=bool(config.get('download_doc', DOWNLOAD_DOC)),
        download_image=bool(config.get('download_image', DOWNLOAD_IMAGE)),
        download_other=bool(config.get('download_other', DOWNLOAD_OTHER)),
        llm_provider=config.get('llm_provider', LLM_PROVIDER),
        api_keys=config.get('openai_api_keys', OPENAI_API_KEYS),
        max_tokens_per_request=int(config.get('max_tokens', MAX_TOKENS)),
        max_urls=int(config.get('max_urls', MAX_URLS)) if config.get('max_urls') else None,
        base_dir=config.get('crawler_output_dir', CRAWLER_OUTPUT_DIR),
        status_callback=status_update_handler
    )

    # Si un fichier de checkpoint personnalisé est fourni
    if 'checkpoint_file' in config:
        crawler.CHECKPOINT_FILE = config['checkpoint_file']

    # Démarrer le crawler dans un thread séparé
    crawler_thread = threading.Thread(target=crawler.crawl)
    crawler_thread.start()

    return jsonify({'status': 'success', 'message': 'Crawler démarré.'})

@app.route('/stop', methods=['POST'])
def stop_crawl():
    global crawler

    if crawler and crawler_thread.is_alive():
        crawler.stop_crawl()
        crawler_thread.join(timeout=10)
        if crawler_thread.is_alive():
            return jsonify({'status': 'error', 'message': 'Échec de l\'arrêt du crawler.'}), 500
        else:
            return jsonify({'status': 'success', 'message': 'Crawler arrêté.'})
    else:
        return jsonify({'status': 'error', 'message': 'Le crawler n\'est pas en cours d\'exécution.'}), 400

@app.route('/status', methods=['GET'])
def get_status():
    # Cet endpoint pourrait retourner l'état actuel si maintenu
    # Alternativement, s'appuyer sur SocketIO pour les mises à jour en temps réel
    return jsonify({'status': 'Utilisez SocketIO pour les mises à jour en temps réel.'})

if __name__ == '__main__':
    # Utiliser eventlet pour le support asynchrone
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
