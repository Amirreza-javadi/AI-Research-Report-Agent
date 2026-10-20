from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Research & Report Agent"
    api_v1_prefix: str = "/api/v1"
    tavily_api_key: str
    # Override this in .env with your MySQL connection string.
    # SQLite default makes the scaffold easy to run before MySQL is configured.
    database_url: str = "sqlite:///./ai_research_agent.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
