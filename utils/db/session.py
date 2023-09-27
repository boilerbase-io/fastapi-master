from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session, sessionmaker

from src.config import Config


engine = create_engine(
    Config.assemble_db_connection(),
    pool_pre_ping=True,
    pool_size=500,
    max_overflow=100,
    pool_recycle=60 * 60,
    pool_timeout=30,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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
