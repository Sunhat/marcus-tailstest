from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

def _get_project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "requirements.txt").exists():
            return parent
    return current.parent

class Settings(BaseSettings):
    app_name: str = "Marcus' Tails Code Test"
    debug: bool = True
    port: int = 8000
    host: str = "0.0.0.0"
    data_dir: Path = _get_project_root() / "data"
    stores_file: Path = data_dir / "stores.json"
    enriched_stores_file: Path = data_dir / "stores_enriched.json"

    model_config = SettingsConfigDict(
        env_file=".env",
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()
