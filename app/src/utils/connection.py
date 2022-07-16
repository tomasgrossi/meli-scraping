from app.src.utils.settings import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = Settings()

DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port

# db_engine = create_engine('mysql://' + DB_USER + ":" + DB_PASS + "@" + DB_HOST + ":" + DB_PORT + "/" + DB_NAME)

Session = sessionmaker(autocommit = False, autoflush = False)

Base = declarative_base()

def get_connection():
    db = Session()
    try:
        yield db
    finally:
        db.close()
