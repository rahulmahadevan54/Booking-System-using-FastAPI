from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
engine = create_engine('sqlite:///booking_app/database/m.db', echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base=declarative_base()
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()