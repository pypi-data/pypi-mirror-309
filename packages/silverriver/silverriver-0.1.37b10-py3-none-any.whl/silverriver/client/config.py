import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

import silverriver

root_dir = pathlib.Path(os.path.dirname(silverriver.__file__)).parent.parent


class Settings(BaseSettings, frozen=True, extra="ignore"):
    model_config = SettingsConfigDict(
        env_file=root_dir / ".env",
        env_file_encoding='utf-8',
        env_prefix="SR_"
    )
    API_HOST: str = "crux.silverstream.ai"
    API_PORT: int = 31337

    @property
    def API_SERVER_URL(self) -> str:
        if self.API_HOST == "localhost":
            protocol = "http"
        else:
            protocol = "https"
        return f"{protocol}://{self.API_HOST}:{self.API_PORT}"


client_settings = Settings()
