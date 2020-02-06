from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from config import config_by_name
from flask_bcrypt import Bcrypt

config = config_by_name[os.getenv('ENV') or 'dev']
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))
flask_bcrypt = Bcrypt()

Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.bind = engine
