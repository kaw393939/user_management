from pydantic_settings import BaseSettings


from builtins import bool, int, property, str
from pathlib import Path
from pydantic import  Field, AnyUrl, DirectoryPath

class Settings(BaseSettings):
    max_login_attempts: int = Field(default=3, description="Background color of QR codes")
    # Server configuration
    server_base_url: AnyUrl = Field(default='http://localhost:8000', description="Base URL of the server")
    server_download_folder: str = Field(default='downloads', description="Folder for storing downloaded files")

    # Security and authentication configuration
    secret_key: str = Field(default="secret-key", description="Secret key for encryption")
    algorithm: str = Field(default="HS256", description="Algorithm used for encryption")
    access_token_expire_minutes: int = Field(default=30000, description="Expiration time for access tokens in minutes")
    admin_user: str = Field(default='admin', description="Default admin username")
    admin_password: str = Field(default='secret', description="Default admin password")
    debug: bool = Field(default=False, description="Debug mode outputs errors and sqlalchemy queries")
    jwt_secret_key: str = "a_very_secret_key"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 Hours
    refresh_token_expire_minutes: int = 1440  # 24 hours for refresh token
    # Database configuration
    #database_url: str = Field(default='postgresql+asyncpg://user:password@postgres/myappdb', description="URL for connecting to the database")

    # Optional: If preferring to construct the SQLAlchemy database URL from components
    postgres_user: str = Field(default='user', description="PostgreSQL username")
    postgres_password: str = Field(default='password', description="PostgreSQL password")
    postgres_server: str = Field(default='postgres', description="PostgreSQL server address")
    postgres_port: str = Field(default='5432', description="PostgreSQL port")
    postgres_db: str = Field(default='myappdb', description="PostgreSQL database name")
    # Discord configuration
    
    send_real_mail: bool = Field(default=False, description="use mock")
    # Email settings for Mailtrap
    smtp_server: str = Field(default='smtp.mailtrap.io', description="SMTP server for sending emails")
    smtp_port: int = Field(default=2525, description="SMTP port for sending emails")
    smtp_username: str = Field(default='your-mailtrap-username', description="Username for SMTP server")
    smtp_password: str = Field(default='your-mailtrap-password', description="Password for SMTP server")
    account_verfiy_destination: str = Field(default='http://localhost:8000/', description="Where to redirect the user after account verification")

# Property to construct the database URL from parts
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        # If your .env file is not in the root directory, adjust the path accordingly.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instantiate settings to be imported in your application
settings = Settings()
