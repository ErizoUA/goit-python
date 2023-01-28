from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


url = f'sqlite+pysqlite:///assistant.db'

engine = create_engine(url, echo=True, future=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
