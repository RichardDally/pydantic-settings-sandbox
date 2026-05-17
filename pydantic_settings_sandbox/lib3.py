from typing import Optional
from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Lib3Params(BaseModel):
    """Parameters required when Lib3 is enabled."""
    dummy: str
    figure: int

class Lib3Config(BaseSettings):
    """Aggregator for Lib3."""
    enabled: bool = False
    conditional_parameters: Optional[Lib3Params] = None

    model_config = SettingsConfigDict(
        env_prefix="LIB3__",
        env_nested_delimiter="__",
        extra="ignore"
    )

    @model_validator(mode='after')
    def check_mandatory_params(self) -> 'Lib3Config':
        if self.enabled and self.conditional_parameters is None:
            raise ValueError("params are required when enabled is True")
        return self
