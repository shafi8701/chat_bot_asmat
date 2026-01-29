import os

class Settings:
    BOT_NAME = os.getenv("BOT_NAME", "Asmat Bot")

settings = Settings()