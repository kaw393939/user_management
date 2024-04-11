from pathlib import Path
from pydantic import  Field, AnyUrl, DirectoryPath
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    max_login_attempts: int = Field(default=3, description="Background color of QR codes")
    # Server configuration
    server_base_url: AnyUrl = Field(default='http://localhost:80', description="Base URL of the server")
    server_download_folder: str = Field(default='downloads', description="Folder for storing downloaded files")

    # Security and authentication configuration
    secret_key: str = Field(default="secret-key", description="Secret key for encryption")
    algorithm: str = Field(default="HS256", description="Algorithm used for encryption")
    access_token_expire_minutes: int = Field(default=30, description="Expiration time for access tokens in minutes")
    admin_user: str = Field(default='admin', description="Default admin username")
    admin_password: str = Field(default='secret', description="Default admin password")
    
    # Database configuration
    database_url: str = Field(default='postgresql+asyncpg://user:password@postgres/myappdb', description="URL for connecting to the database")

    # Optional: If preferring to construct the SQLAlchemy database URL from components
    postgres_user: str = Field(default='user', description="PostgreSQL username")
    postgres_password: str = Field(default='password', description="PostgreSQL password")
    postgres_server: str = Field(default='localhost', description="PostgreSQL server address")
    postgres_port: str = Field(default='5432', description="PostgreSQL port")
    postgres_db: str = Field(default='myappdb', description="PostgreSQL database name")

    class Config:
        # If your .env file is not in the root directory, adjust the path accordingly.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings to be imported in your application
settings = Settings()
