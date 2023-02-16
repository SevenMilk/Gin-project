from pydantic import BaseSettings, Field, SecretStr


class DBParams(BaseSettings):
    db_username: SecretStr = Field(..., env="DB_USERNAME")
    db_password: SecretStr = Field(..., env="DB_PASSWORD")
    db_host: SecretStr = Field(..., env="DB_HOST")
    db_database: str = Field(..., env="DB_DATABASE")
    db_table: str = Field(..., env="DB_TABLE")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = 'python/.env_db'
        env_file_encoding = 'utf-8'
