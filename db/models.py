from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "mysql+pymysql://root@localhost:3306/sales_agent"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))        
    company = Column(String(255))    

    interactions = relationship("Interaction", back_populates="prospect") 


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    prospect_id = Column(Integer, ForeignKey("prospects.id"))  

    email = Column(Text)
    reply = Column(Text)
    response = Column(Text)

    prospect = relationship("Prospect", back_populates="interactions")  