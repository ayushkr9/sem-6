from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    summary = Column(String)
    authors = Column(String)
    source = Column(String)
    citations = Column(Integer, default=0)  # Ensure this is an integer
    year = Column(Integer, default=2020)  # New field
    doi = Column(String)
    journal = Column(String)
    publisher = Column(String)
    url = Column(String)

engine = create_engine("sqlite:///research_papers.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print(" database succcesful completed ")