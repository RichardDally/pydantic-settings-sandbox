# pydantic-settings-sandbox

This documentation explains the modular configuration architecture designed for a Python 3.11+ environment using `uv`, `pydantic-settings`, and a hierarchical composition pattern.

This project implements a **Decoupled Configuration Pattern**. Instead of a single, monolithic configuration file, each library defines its own settings and requirements. The main application then aggregates these into a single, type-safe tree.

## Architecture Overview

The architecture follows a tree structure where the `AppConfig` acts as the root. Each branch represents a library, and each leaf represents a specific service configuration (e.g., Database, Cache).

### Key Design Principles

1. **Leaf-Level Isolation:** Every sub-configuration (like `DBConfig`) defines its own `env_prefix`. This ensures that even if two libraries require a "host" parameter, they will not collide (e.g., `LIB1_DB__HOST` vs `LIB2_ANALYTICS__HOST`).
2. **Secret Protection:** Sensitive fields are typed as `SecretStr`. They are automatically masked (replaced with `**********`) during logging and JSON dumping to prevent accidental leaks in production logs.
3. **Strict Validation:** The application will fail fast. If a mandatory environment variable is missing or of the wrong type (e.g., a string provided for a port), the application will log a clean error and exit before starting any services.
4. **Flat Env to Nested Object:** We use `env_nested_delimiter="__"` to bridge the gap between flat environment variables and nested Python objects.

---

## File Structure

* `pyproject.toml`: Manages dependencies via `uv`.
* `lib1.py`: Contains configurations for persistence services (DB, Cache).
* `lib2.py`: Contains configurations for external analytics.
* `app.py`: The entry point that aggregates all libraries.
* `.env`: The local environment file where values are defined.

---

## Usage: The `app.py` Perspective

As an application developer, you only interact with the `AppConfig` object. You do not need to manually parse `.env` files or handle type casting.

### 1. Initialization

At the start of your application, call the `bootstrap()` function. This function performs the following:

* Loads values from the environment.
* Validates all types and mandatory fields.
* Logs the loaded (and masked) configuration for debugging.

```python
from app import bootstrap

# Load all settings at once
cfg = bootstrap()

# Accessing parameters is now fully typed with IDE autocompletion
print(f"Starting {cfg.app_name}...")

```

### 2. Accessing Settings

The settings are accessible via standard Python dot notation. This is highly beneficial for IDEs, providing full autocompletion and type checking.

```python
# Accessing Lib1 Database
db_host = cfg.lib1.db.host
db_pass = cfg.lib1.db.password.get_secret_value()  # Explicitly reveal secret

# Accessing Lib2 Analytics
api_key = cfg.lib2.analytics.api_key

```

### 3. Handling Configuration Errors

If the configuration is invalid, the bootstrap process will intercept the `ValidationError` and output a human-readable log:

```text
ERROR: !!! Configuration Validation Failed !!!
ERROR:   lib1 -> db -> host: Field required
ERROR:   lib1 -> db -> password: Field required
ERROR:   lib2 -> analytics -> api_key: Field required
CRITICAL: Application startup aborted.

```

---

## Environment Variable Reference

To configure the application, create a `.env` file in the root directory. Values are mapped according to the `env_prefix` defined in each sub-configuration.

| Environment Variable | Python Path | Description |
| --- | --- | --- |
| `APP_NAME` | `cfg.app_name` | The name of the application |
| `LIB1_DB__HOST` | `cfg.lib1.db.host` | Database server address |
| `LIB1_DB__USER` | `cfg.lib1.db.user` | Database username |
| `LIB1_DB__PASSWORD` | `cfg.lib1.db.password` | Database password (Secret) |
| `LIB1_CACHE__REDIS_URL` | `cfg.lib1.cache.redis_url` | Redis connection string |
| `LIB2_ANALYTICS__API_KEY` | `cfg.lib2.analytics.api_key` | Third-party API token |

---

## Development Setup

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run the application
uv run app.py

```