"""Define application settings"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    """Application settings class"""
    model_config = SettingsConfigDict(
        env_file=".env", # Read from ".env" file
        env_file_encoding="utf-8", # Default
        env_prefix="CLONE_KIOT_VIET_", # Default to "" (no prefix)
        extra="ignore") # Ignore extra environment variables that are not defined in the model

    # Define your settings attributes here
    # Database settings
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:sh1n1ch1@127.0.0.1:3306/clone_kiot_viet"
    DATABASE_NAME: str = "clone_kiot_viet"

    # Authentication and Authorization settings
    SECRET_KEY: str = "mFJfs02fg2bMrEhTnIHdYCQ99hYwfaO5"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    TOKEN_TYPE: str = "Bearer"
    ISSUER: str = "clone_kiot_viet--backend"
    AUDIENCE: str = "clone_kiot_viet--frontend"

    # Session settings
    SESSION_EXPIRE_MINUTES: int = 43200  # 30 days

    # Admin user settings
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@datvipcrvn.com"
    ADMIN_INITIAL_PASSWORD: str = "Admin@123!"  # Default password for the admin user
    ADMIN_DISPLAY_NAME: str = "Administrator"  # Default display name for the admin user
    

settings = Setting()
