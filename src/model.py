from sqlalchemy import Integer,String,Column,ForeignKey
#my local database file se base ko import kiya
from .database import Base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    startup_idea = Column(String, nullable=False)

    # Evaluation fields
    creativity_sentence = Column(String)
    creativity_score = Column(Integer)

    demand_sentence = Column(String)
    demand_score = Column(Integer)

    uniqueness_sentence = Column(String)
    uniqueness_score = Column(Integer)

    scale_sentence = Column(String)
    scale_score = Column(Integer)

    investment_sentence = Column(String)
    investment_score = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    thinker = relationship("User", back_populates="ideas")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True,index=True)
    username = Column(String)
    password = Column(String)
    num_ideas = Column(Integer)
    ideas = relationship("Idea" , back_populates= "thinker")