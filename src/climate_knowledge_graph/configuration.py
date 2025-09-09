"""
Configuration module
"""

import os

import diskcache
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    NEO4J_URL: str = "localhost"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "your_password"
    MISTRAL_API_KEY: str | None = None
    MISTRAL_MODEL: str = "mistral-medium"
    DISK_CACHE_DIRECTORY: str | None = None

    def get_mistral_api_key(self) -> str:
        if self.MISTRAL_API_KEY is None:
            raise EnvironmentError("No MISTRAL_API_KEY defined in environment")
        return self.MISTRAL_API_KEY

    @property
    def disk_cache(self) -> diskcache.Cache:
        if self.DISK_CACHE_DIRECTORY is None:
            raise EnvironmentError("No DISK_CACHE_DIRECTORY defined in environment")
        return diskcache.Cache(directory=os.path.expanduser(self.DISK_CACHE_DIRECTORY))
