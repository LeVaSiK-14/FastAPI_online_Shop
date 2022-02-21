from sqlalchemy.orm import declarative_base,  sessionmaker
from sqlalchemy import create_engine

engine=create_engine(
            "postgresql://fastapiuser:fastapipassword@localhost:5432/fastapidb",  
            echo=True
)

Base = declarative_base()

SessionLocal=sessionmaker(bind=engine)