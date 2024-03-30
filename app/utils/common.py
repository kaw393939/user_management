from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))
FILL_COLOR = os.getenv('FILL_COLOR', 'red')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
            },
        },
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console'],
                'level': 'INFO'
            },
        }
    })

def create_directory():
    try:
        QR_DIRECTORY.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {QR_DIRECTORY}: {e}")
        raise
