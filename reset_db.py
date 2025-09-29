# backend/reset_db.py
import os
from sqlmodel import SQLModel, create_engine
from models import Draft

def reset_database():
    """Reset the database with the new schema"""
    # Get the backend directory path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(backend_dir, "database.db")
    
    # Remove existing database file
    if os.path.exists(database_path):
        os.remove(database_path)
        print(f"Removed existing database at {database_path}")
    
    # Create new database with updated schema
    engine = create_engine(f"sqlite:///{database_path}")
    SQLModel.metadata.create_all(engine)
    print(f"Created new database with updated schema at {database_path}")

if __name__ == "__main__":
    reset_database() 