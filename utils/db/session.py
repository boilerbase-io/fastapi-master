from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import ProgrammingError

from sqlalchemy import create_engine

from src.config import Config


def get_db_seed():
    try:
        db = SessionLocal()
    except Exception as err:
        print(f"Exception Raised: {str(err)}")
        return None
    return db


def _get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db

    except ProgrammingError as pe:
        print("###############################################")
        print("EITHER DATABASE NOT FOUND OR NO TABLES PRESENT")
        print("###############################################")
        return pe
    finally:
        db.close()


get_db = Annotated[Session, Depends(_get_db)]

engine = create_engine(
    Config.assemble_db_connection(),
    pool_pre_ping=True,
    pool_size=500,
    max_overflow=100,
    pool_recycle=60 * 60,
    pool_timeout=30,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
