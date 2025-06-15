from sqlalchemy import Integer,String,Column,ForeignKey
#my local database file se base ko import kiya
from .database import Base
from sqlalchemy.orm import relationship

class Ideas(Base):
    __tablename__ = "ideas"
    id = Column(Integer, primary_key=True , index=True)
    content = Column(String)
    user_id =Column(Integer , ForeignKey('user.id'))
    #users beacuse of tablename

    thinker = relationship("User",back_populates="ideas")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key=True,index=True)
    username = Column(String)
    password = Column(String)

    ideas = relationship("Ideas" , back_populates= "thinker")