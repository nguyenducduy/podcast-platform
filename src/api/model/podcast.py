from db import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.event import listens_for
import pendulum


class Podcast(Base):
    __tablename__ = 'podcast'

    id = Column(Integer, primary_key=True, autoincrement=True)
    u_id = Column(Integer)
    title = Column(String(255))
    author = Column(String(150))
    cover = Column(String(255))
    description = Column(String)
    keywords = Column(String)
    status = Column(Integer)
    language = Column(Integer)
    contact_email = Column(String(150))
    website_url = Column(String(255))
    copyright = Column(String(100))
    rss_link = Column(String(255))
    apple_rss_link = Column(String(255))
    apple_rss_file = Column(String(255))
    created_at = Column(Integer, nullable=False)
    updated_at = Column(Integer)

    STATUS_PUBLISH = 1
    STATUS_DRAFT = 3
    LANGUAGE_VI = 1
    LANGUAGE_EN = 3

@listens_for(Podcast, 'before_insert')
def generate_created_at(mapper, connect, self):
    self.created_at = int(pendulum.now().timestamp())
    return self.created_at

@listens_for(Podcast, 'before_update')
def generate_updated_at(mapper, connect, self):
    self.updated_at = int(pendulum.now().timestamp())
    return self.updated_at
