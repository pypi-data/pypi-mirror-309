from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import db_url

engine = create_engine(db_url, pool_size=10, max_overflow=20, pool_recycle=10, pool_timeout=10)
Session = sessionmaker(bind=engine)