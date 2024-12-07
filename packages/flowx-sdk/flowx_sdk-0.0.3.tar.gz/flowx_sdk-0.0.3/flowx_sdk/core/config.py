from pydantic_settings import ( #type: ignore
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict
)
from pydantic import Field #type: ignore

class Settings(BaseSettings):
    base_url: str

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )

    @classmethod
    def settings_customise_sources(
        cls, settings_cls: type[BaseSettings],
          init_settings: PydanticBaseSettingsSource, 
          env_settings: PydanticBaseSettingsSource, 
          dotenv_settings: PydanticBaseSettingsSource, 
          file_secret_settings: PydanticBaseSettingsSource) -> tuple[PydanticBaseSettingsSource, ...]:
        return super().settings_customise_sources(
            settings_cls, init_settings, 
            env_settings, dotenv_settings, file_secret_settings)
    

# Instantiate the settings
settings = Settings() #type: ignore