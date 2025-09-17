from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from ..contants import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column((Integer), primary_key=True, autoincrement=True, nullable=False)
    difficulty = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.now)
    created_by = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    correct_answer_id = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)
    

class ChallengeQuota(Base):
    __tablename__ = "challenge_quotas"
    
    id = Column((Integer), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(String, nullable=False, unique=True)
    quota_remaining = Column(Integer, nullable=False, default=50)
    last_reset_date = Column(DateTime, nullable=False, default=datetime.now)
    

