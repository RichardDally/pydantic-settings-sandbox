from pydantic_settings import BaseSettings, SettingsConfigDict

class AnalyticsConfig(BaseSettings):
    api_key: str
    endpoint: str = "https://analytics.io"

    model_config = SettingsConfigDict(
        env_prefix="LIB2_ANALYTICS__",
        extra="ignore"
    )

class Lib2Config(BaseSettings):
    """Aggregator for Lib2."""
    analytics: AnalyticsConfig = AnalyticsConfig()
