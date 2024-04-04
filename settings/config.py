from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):
    # QR code directory configuration
    qr_directory: Path = Path('./qr_codes')

    # QR code appearance configuration
    fill_color: str = 'red'
    back_color: str = 'white'

    # Server configuration
    server_base_url: str = 'http://localhost:80'
    server_download_folder: str = 'downloads'

    # Security and authentication configuration
    secret_key: str = "secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_user: str = 'admin'
    admin_password: str = 'secret'

    # Database configuration
    database_url: str = 'postgresql://user:password@localhost/myappdb'

    # Optional: If preferring to construct the SQLAlchemy database URL from components
    postgres_user: str = 'user'
    postgres_password: str = 'password'
    postgres_server: str = 'localhost'
    postgres_port: str = '5432'  # default PostgreSQL port
    postgres_db: str = 'myappdb'

    class Config:
        # If your .env file is not in the root directory, adjust the path accordingly.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings to be imported in your application
settings = Settings()
