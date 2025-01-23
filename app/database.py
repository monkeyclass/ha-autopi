import os
from sqlmodel import SQLModel, create_engine, Session

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, '../data')
os.makedirs(data_dir, exist_ok=True)

sqlite_file_name = os.path.join(data_dir, "database.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)