# 📌 FastAPI Project Template

## 🚀 Introduction
This project is a modular FastAPI template designed to quickly start developing a REST API with authentication, database management, and structured project organization.

---

## 📂 Project Structure
```
myproject/  # Replace 'myproject' with your project name
├── README.MD
├── alembic/
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── alembic.ini
├── api/
│   └── v1/
│       ├── api_v1.py
│       └── endpoints/
│           ├── auth.py      # Example authentication endpoint
│           ├── example.py   # Example generic endpoint
│           ├── protected.py # Example protected endpoint
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── init_project.py
├── main.py
├── middlewares/
│   ├── auth_middleware.py
│   └── role_middleware.py
├── models/
│   ├── base.py
│   └── user.py
├── requirements.txt
├── schemas/
│   └── user.py
├── tests/
│   ├── test_main.py
│   ├── test_auth.py
│   ├── test_protected.py
│   ├── __init__.py
│── Dockerfile
└── docker-compose.yml
```

📌 **Note:** The `auth.py`, `example.py`, and `protected.py` endpoints are provided as examples. You can modify or remove them based on your project requirements.

---

## 🛠 How to Use the Template
### 1️⃣ Clone the repository
```sh
git clone https://github.com/username/myproject.git  # Replace 'myproject' with your project name
cd myproject
```

### 2️⃣ Create a virtual environment and install dependencies
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install --upgrade pip
pip install -r requirements.txt
pip install --force-reinstall --no-cache-dir bcrypt
pip install --force-reinstall --no-cache-dir passlib
```

### 3️⃣ Initialize the project
Run the initialization script to configure the database, generate a new `SECRET_KEY`, and set up the project:
```sh
python init_project.py myproject  # Replace 'myproject' with your project name
```
This script will also **create two default users**:
- **Admin user**: `admin@example.com` with password `admin123`
- **Normal user**: `user@example.com` with password `password123`

These users are created only if they do not already exist in the database.

### 4️⃣ Run the application
```sh
uvicorn main:app --reload  # Replace 'myproject' with your project name
```
The API is accessible at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🗄 Database Configuration (SQLite, MySQL, PostgreSQL)
By default, the project uses SQLite. To switch to MySQL or PostgreSQL, modify the `.env` file with your database credentials:

**.env file:**
```ini
DB_TYPE=postgresql  # Use 'sqlite', 'mysql', or 'postgresql'
DB_USER=user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=mydatabase
```
The database settings are automatically loaded in `core/config.py`:
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "bp_fastapi")
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Apply migrations
If using Alembic, generate and apply migrations:
```sh
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## 🐍 Database Migrations with Alembic
### 1️⃣ Initialize Alembic
```sh
alembic init alembic
```
This creates an `alembic/` folder to manage database versions.

### 2️⃣ Generate a migration after modifying models
```sh
alembic revision --autogenerate
```

### 3️⃣ Apply the migration
```sh
alembic upgrade head
```

### 4️⃣ Rollback a migration
```sh
alembic downgrade -1
```

---

## ✅ Testing
The project includes basic tests using `pytest` and `httpx`. Ensure you have installed the required testing dependencies:
```sh
pip install pytest==8.3.4 httpx==0.28.1
```

Run tests with:
```sh
TESTING=True pytest tests/
```

### 🔹 **Included Tests:**
- **`test_main.py`**: Basic health check of the API.
- **`test_auth.py`**: Tests for user authentication (login success & failure).
- **`test_protected.py`**: Tests access to protected routes using JWT tokens.

Example of running tests:
```sh
pytest tests/
```
If all tests pass, you should see output indicating successful test execution.

---

## 📜 License
This project is licensed under the MIT License. Free to use and modify. 🎉

