# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    class Config:
        from_attributes = True
    API_KEY: str = "SL170030662"
    CRM_API_URL: str = "https://challenge.berrydev.ai/api/crm/customers"
    MARKETING_API_URL: str = "https://challenge.berrydev.ai/api/marketing/campaigns"
    DATABASE_URL: str = "sqlite+aiosqlite:///./warehouse.db"

settings = Settings()
