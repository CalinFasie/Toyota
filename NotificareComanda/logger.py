# logger.py
import logging

# Configurare logger
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message):
    """Înregistrează un mesaj informativ în log."""
    logging.info(message)

def log_error(message):
    """Înregistrează un mesaj de eroare în log."""
    logging.error(message)
