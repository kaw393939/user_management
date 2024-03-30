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
BACK_COLOR = os.getenv('BACK_COLOR', 'white')
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')


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

def create_directory(directory_path):
    """Create a directory if it does not exist."""
    try:
        # Using os.makedirs to create the directory if it does not exist.
        # exist_ok=True prevents raising an exception if the directory already exists.
        os.makedirs(directory_path, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {directory_path}: {e}")
        # Rethrow the exception to handle it further up the call stack.
        raise