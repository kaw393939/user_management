# Load environment variables
import os
from pathlib import Path
from dotenv import load_dotenv

# The dotenv package is used to load environment variables from a .env file
# into the environment for this script. This is useful for keeping secrets out of source code.
load_dotenv()

# Environment Variables for Configuration

# QR_DIRECTORY specifies the directory where QR codes are saved.
# If not specified in the environment, it defaults to './qr_codes'.
QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))

# FILL_COLOR determines the color of the QR code itself. Defaults to 'red'.
FILL_COLOR = os.getenv('FILL_COLOR', 'red')

# BACK_COLOR sets the background color of the QR code. Defaults to 'white'.
BACK_COLOR = os.getenv('BACK_COLOR', 'white')

# SERVER_BASE_URL is the base URL for the server. This might be used for constructing
# URLs in responses. Defaults to 'http://localhost:80'.
SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')

# SERVER_DOWNLOAD_FOLDER specifies the directory exposed by the server for downloads,
# such as QR codes. This could be a path routed by your server for static files.
SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

# SECRET_KEY is used in cryptographic operations, such as signing JWT tokens. 
# It should be a long, random string that is kept secret.
SECRET_KEY = os.getenv("SECRET_KEY", "secret-getenvkey")

# ALGORITHM specifies the algorithm used for JWT encoding/decoding.
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# ACCESS_TOKEN_EXPIRE_MINUTES defines how long (in minutes) an access token remains valid.
# Defaults to 30 minutes.
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ADMIN_USER and ADMIN_PASSWORD are placeholder credentials for basic authentication
# in this example. In production, use a more secure authentication method.
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')
