from sqlmodel import SQLModel, create_engine
from config import get_settings

settings = get_settings()

engine = create_engine(f"sqlite:///{settings.sqlite_path}")
