import os
import logging
import subprocess
import requests
from jupyter_server.extension.application import ExtensionApp
from IPython.display import display, Javascript

# Set up logging
logger = logging.getLogger("my_extension_logger")
logger.setLevel(logging.DEBUG)

def log_to_browser(message):
    """Send log messages to the browser console."""
    display(Javascript(f'console.log("{message}");'))

def download_ollama():
    """Download Ollama if not already present."""
    # ollama_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../shared/ollama"));
    ollama_path = os.path.abspath("/shared/jupyterlab-a11y-checker/ollama")
    if not os.path.exists(ollama_path):
        logger.info("Ollama not found. Downloading...")
        log_to_browser("Ollama not found. Downloading...")

        # Download Ollama (Linux AMD64 version) on a hub environment
        url = "https://github.com/ollama/ollama/releases/download/v0.3.6/ollama-linux-amd64"
        # url = "https://github.com/ollama/ollama/releases/download/v0.3.6/ollama-darwin"
        response = requests.get(url)
        
        # Save the downloaded file as 'ollama'
        with open(ollama_path, "wb") as file:
            file.write(response.content)
        
        # Make it executable
        os.chmod(ollama_path, 0o755)
        logger.info("Ollama downloaded and set to executable.")
        log_to_browser("Ollama downloaded and set to executable.")
    else:
        logger.info("Ollama is already present.")
        log_to_browser("Ollama is already present.")

def run_ollama():
    """Run Ollama."""
    logger.info("Starting Ollama...")
    log_to_browser("Starting Ollama...")

    try:
        # If on a hub environment -> ollama_path = os.path.abspath("/mnt/shared/ollama")?
        # ollama_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../shared/ollama"));
        ollama_path = os.path.abspath("/shared/jupyterlab-a11y-checker/ollama")
        subprocess.Popen([ollama_path, "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen([ollama_path, "run", "llava:13b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Ollama started successfully.")
        log_to_browser("Ollama started successfully.")
    except Exception as e:
        logger.error(f"Error starting Ollama: {e}")
        log_to_browser(f"Error starting Ollama: {e}")

def load_jupyter_server_extension(app):
    """Load the server extension."""
    logger.info("Extension has started.")
    log_to_browser("Extension has started in the browser console.")

    # Download Ollama if not present
    download_ollama()

    # Run Ollama
    run_ollama()