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

settings = Setting()
