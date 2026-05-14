from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DBConfig(BaseSettings):
    host: str = "localhost"
    user: str
    password: SecretStr

    model_config = SettingsConfigDict(
        env_prefix="LIB1_DB__", # Specific prefix
        extra="ignore"
    )

class CacheConfig(BaseSettings):
    redis_url: str = "redis://localhost:6379"

    model_config = SettingsConfigDict(
        env_prefix="LIB1_CACHE__", # Specific prefix
        extra="ignore"
    )

class Lib1Config(BaseSettings):
    """Aggregator for Lib1 using sub-config prefixes."""
    db: DBConfig = Field(default_factory=DBConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
