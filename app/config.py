import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file into the environment.
load_dotenv()

# QR code directory configuration
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))

# QR code appearance configuration
FILL_COLOR = os.getenv('FILL_COLOR', 'red')
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

# Server configuration
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

# Security and authentication configuration
SECRET_KEY = os.getenv("SECRET_KEY", "secret-getenvkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')

# Database configuration
# Utilize DATABASE_URL for a more dynamic setup or decompose into individual components
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres/myappdb')
# If preferring to decompose, use these instead
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')  # default PostgreSQL port
POSTGRES_DB = os.getenv('POSTGRES_DB', 'myappdb')

# Constructing the SQLAlchemy database URL from components if needed
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
