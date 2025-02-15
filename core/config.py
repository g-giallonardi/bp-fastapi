import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "bp_fastapi")
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite/mysql/postgresql

    if "pytest" in os.environ.get("_", "") or os.getenv("TESTING"):
        DB_TYPE = os.getenv("TEST_DB_TYPE", "sqlite")
        DB_NAME = os.getenv("TEST_DB_NAME", "test")

    if DB_TYPE == "sqlite":
        DATABASE_URL = f"sqlite:///./{DB_NAME}.db"
    elif DB_TYPE == "mysql":
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    elif DB_TYPE == "postgresql":
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        raise ValueError("DB_TYPE non supporté, utilise 'sqlite', 'mysql' ou 'postgresql'.")

settings = Settings()