import os
from dotenv import load_dotenv

load_dotenv() 

class Settings:
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME", "bp_fastapi")
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # sqlite/mysql/postgresql

    if "pytest" in os.environ.get("_", "") or os.getenv("TESTING"):
        DB_USER = os.getenv("TEST_DB_USER", "test_user")
        DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", "test_password")
        DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
        DB_PORT = os.getenv("TEST_DB_PORT")
        DB_NAME = os.getenv("TEST_DB_NAME", "test_bp_fastapi")
        DB_TYPE = os.getenv("TEST_DB_TYPE", "sqlite")

    print(f"DB_TYPE: {DB_TYPE}")
    print(f"DB_USER: {DB_USER}")
    print(f"DB_PASSWORD: {DB_PASSWORD}")
    print(f"DB_HOST: {DB_HOST}")
    print(f"DB_PORT: {DB_PORT}")
    print(f"DB_NAME: {DB_NAME}")
    
    if DB_TYPE == "sqlite":
        DATABASE_URL = f"sqlite:///./{DB_NAME}.db"
    elif DB_TYPE == "mysql":
        DB_PORT = DB_PORT or "3306"
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif DB_TYPE == "postgresql":
        DB_PORT = DB_PORT or "5432"
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(DATABASE_URL)
    else:
        raise ValueError("DB_TYPE non supporté, utilise 'sqlite', 'mysql' ou 'postgresql'.")

settings = Settings()