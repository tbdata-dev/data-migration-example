from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///example.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

# create the database tables from the models
def init_db():
    Base.metadata.create_all(bind=engine)