from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class SystemSettings(BaseModel):
    debug: bool = False
    language: str = "en"


class SpotifySettings(BaseModel):
    url: str = "https://open.spotify.com/track/"


class TelegramSettings(BaseModel):
    api_id: int
    api_hash: str
    target_user_id: int
    session: str = "session"
    parse_mode: str = "html"
    link_preview: bool = False


class Settings(BaseSettings):
    system: SystemSettings = SystemSettings()
    spotify: SpotifySettings = SpotifySettings()
    tg: TelegramSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP__",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


settings = Settings()  # noqa
