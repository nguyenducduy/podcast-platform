import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy(current_app)

# engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'],
#                        convert_unicode=True, pool_pre_ping=True, pool_recycle=3600)
# db_session = scoped_session(sessionmaker(
#     autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))
# BaseModel = declarative_base()
# BaseModel.query = db_session.query_property()
# BaseModel.metadata.bind = engine
