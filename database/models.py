from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os

Base = declarative_base()


class JobOffer(Base):
    __tablename__ = "job_offers"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    title         = Column(String(255), nullable=False)
    company       = Column(String(255))
    location      = Column(String(100))
    contract_type = Column(String(50))
    experience    = Column(String(100))
    description   = Column(Text)
    skills        = Column(Text)
    source        = Column(String(50))
    url           = Column(String(500), unique=True)
    date_posted   = Column(String(50))
    date_scraped  = Column(DateTime, default=datetime.now)


def get_engine(db_path="data/jobs.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)
    return engine