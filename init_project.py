import os
import sys
import secrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import Base
from models.user import User
from core.security import hash_password

OLD_NAME = "bp_fastapi"  # Nom du template de base
SECRET_KEY_LENGTH = 32   # Longueur de la SECRET_KEY

DATABASE_URL = "sqlite:///./bp_fastapi.db"  # Base SQLite par défaut

def generate_secret_key():
    """Génère une SECRET_KEY aléatoire"""
    return secrets.token_hex(SECRET_KEY_LENGTH)

def rename_project(new_name, root_dir="."):
    """Renomme le projet et met à jour les fichiers"""
    
    old_path = os.path.join(root_dir, OLD_NAME)
    new_path = os.path.join(root_dir, new_name)

    # Étape 1: Renommer le dossier principal
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"✅ Dossier renommé : {OLD_NAME} → {new_name}")
    else:
        print(f"⚠️ Dossier {OLD_NAME} introuvable ! Vérifie ton emplacement.")
        return

    # Étape 2: Remplacer les imports et références dans les fichiers `.py`
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content.replace(f"import {OLD_NAME}", f"import {new_name}")\
                                     .replace(f"from {OLD_NAME}", f"from {new_name}")

                if new_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"🔄 Modifié : {file_path}")

    # Étape 3: Générer une nouvelle SECRET_KEY et l'insérer dans core/security.py
    security_file = os.path.join(new_path, "core", "security.py")
    
    if os.path.exists(security_file):
        new_secret_key = generate_secret_key()
        with open(security_file, "r", encoding="utf-8") as f:
            security_content = f.read()
        
        updated_security_content = security_content.replace(
            'SECRET_KEY = "my_secret_key"', f'SECRET_KEY = "{new_secret_key}"'
        )

        with open(security_file, "w", encoding="utf-8") as f:
            f.write(updated_security_content)

        print(f"🔑 Nouvelle SECRET_KEY générée dans {security_file}")

    print("✅ Renommage terminé !")

def init_database():
    """Crée la base de données et ajoute les utilisateurs de test"""
    print("📦 Initialisation de la base de données...")

    # Connexion à la base de données
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Création des tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Vérifier si les utilisateurs existent déjà
    if not db.query(User).filter_by(email="admin@example.com").first():
        admin_user = User(email="admin@example.com", password=hash_password("admin123"), role="admin")
        db.add(admin_user)

    if not db.query(User).filter_by(email="user@example.com").first():
        normal_user = User(email="user@example.com", password=hash_password("password123"), role="user")
        db.add(normal_user)

    db.commit()
    db.close()
    print("✅ Base de données initialisée avec succès !")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("❌ Usage : python init_project.py <nouveau_nom>")
    #     sys.exit(1)

    # new_name = sys.argv[1]

    # rename_project(new_name)
    init_database()