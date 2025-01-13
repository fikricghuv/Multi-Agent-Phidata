from dotenv import load_dotenv
import os

def load_environment_variables():
    load_dotenv()
    return {
        "PHI_API_KEY": os.getenv("PHI_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "BASE_URL": os.getenv("BASE_URL"),
        "HOST": os.getenv("HOST"),
        # "PORT": os.getenv("PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("USER"),
        "PASSWORD": os.getenv("PASSWORD"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_API_URL": os.getenv("TELEGRAM_API_URL")
    }