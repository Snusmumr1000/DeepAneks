from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

engine = create_engine('sqlite:///aneks.db')
Base = declarative_base()


class Anek(Base):
    __tablename__ = 'aneks'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    likes = Column(Integer)
    best = Column(Boolean, default=False)
    pub = Column(String)


class Best(Base):
    __tablename__ = 'best_aneks'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    likes = Column(Integer)
    pub = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
