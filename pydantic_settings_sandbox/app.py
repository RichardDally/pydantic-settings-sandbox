import logging
import sys
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from lib1 import Lib1Config
from lib2 import Lib2Config

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class AppConfig(BaseSettings):
    app_name: str = "EnterpriseApp"

    # These will trigger the internal loading of sub-configs
    # using their specific prefixes.
    lib1: Lib1Config = Lib1Config()
    lib2: Lib2Config = Lib2Config()

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


def bootstrap() -> AppConfig:
    try:
        settings = AppConfig()
        logger.info("Configuration aggregation complete.")
        # Native Pydantic masking
        logger.info(settings.model_dump_json(indent=2))
        return settings
    except ValidationError as e:
        logger.error("!!! Configuration Validation Failed !!!")
        for error in e.errors():
            # In this 'prefix' mode, we look for the last part of the location
            # to help the user identify the field.
            field_path = " -> ".join(str(p) for p in error["loc"])
            logger.error(f"  ❌ {field_path}: {error['msg']}")
        sys.exit(1)


if __name__ == "__main__":
    cfg = bootstrap()
    cfg.app_name