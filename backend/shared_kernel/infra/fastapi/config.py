from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:sh1n1ch1@127.0.0.1:3306/clone_kiot_viet"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Setting()