from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Setting_base(BaseSettings):
    
    DBPG_HOST: str
    DBPG_PORT: str
    DBPG_USER: str
    DBPG_PASS: str
    DBPG_NAME: str

    DATABASEPG_URL: str | None = None

    @model_validator(mode="after")
    def get_base_pg(self):
        self.DATABASEPG_URL = f"postgresql+asyncpg://{self.DBPG_USER}:{self.DBPG_PASS}@{self.DBPG_HOST}:{self.DBPG_PORT}/{self.DBPG_NAME}"
        return self
    
    model_config= SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    HASED: str
    HASED_CODING: str

setbase = Setting_base()

#print(setbase.DATABASEPG_URL)