from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models import JobOffer, get_engine
import pandas as pd


def save_offers(offers, db_path="data/jobs.db"):
    engine = get_engine(db_path)
    saved = 0
    with Session(engine) as session:
        for offer in offers:
            job = JobOffer(**offer)
            try:
                session.add(job)
                session.commit()
                saved += 1
            except IntegrityError:
                session.rollback()
    print(f"💾 {saved} nouvelles offres sauvegardées ({len(offers) - saved} doublons ignorés)")
    return saved


def load_offers(db_path="data/jobs.db"):
    engine = get_engine(db_path)
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM job_offers ORDER BY date_scraped DESC", conn)
    return df


def count_offers(db_path="data/jobs.db"):
    engine = get_engine(db_path)
    with Session(engine) as session:
        return session.query(JobOffer).count()