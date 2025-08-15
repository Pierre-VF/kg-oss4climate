import pydantic_settings
from dotenv import load_dotenv

load_dotenv()


class Settings(pydantic_settings.BaseSettings):
    NEO4J_URL: str = "localhost"
    NEO4J_USERNAME: str = "neo4j"
    NEO4J_PASSWORD: str = "your_password"
