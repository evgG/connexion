# coding=utf-8
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def init_db(uri):
    engine = create_engine(uri, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

    return db_session


class Hero(Base):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def serialize(self):
        return dict(id=self.id, name=self.name,)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password
