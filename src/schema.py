
from pydantic import BaseModel
from typing import List, Optional

# for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    usid: Optional[int] = None

# for system user
class baseUser(BaseModel):
    usid: int
    username: str
    password: str 
    num_ideas: int

# for user creation
class User(BaseModel):
    username: str
    password: str

# for user responses
class showUser(BaseModel):
    id: int  # Added 'id' to match your User model
    username: str
    num_ideas: int

    class Config:
        from_attributes = True

class input_Ideas(BaseModel):
    startup_idea: str


# This is the corrected version of showIdea.
# It has been flattened to directly match the fields in your database's Idea model.
class showIdea(BaseModel):
    id: int
    startup_idea: str

    creativity_sentence: str
    creativity_score: int

    demand_sentence: str
    demand_score: int

    uniqueness_sentence: str
    uniqueness_score: int

    scale_sentence: str
    scale_score: int

    investment_sentence: str
    investment_score: int
    
    # The 'thinker' relationship should still work as a nested model
    # because SQLAlchemy handles the relationship correctly.
    thinker: showUser

    class Config:
        from_attributes = True