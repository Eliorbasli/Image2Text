# common/config.py
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Pydantic v2 settings config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    # App
    app_name: str = "image2text"
    env: str = Field(default="local", description="local | docker | prod")

    # Storage
    sqlite_path: str = Field(default=str(Path("data") / "app.db"))
    upload_dir: str = Field(default=str(Path("data") / "uploads"))

    # RabbitMQ
    amqp_url: str = Field(default="amqp://guest:guest@localhost:5672/")
    queue_name: str = Field(default="image_jobs")
    routing_prefix: str = Field(default="app")
    
    # API Ninjas key
    api_ninjas_key: str = Field(default="", description="API Ninjas key from .env (API_NINJAS_KEY)")

    


settings = Settings()
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
