from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    usid: int | None = None


#for system
class baseUser(BaseModel):
    usid:int
    username: str
    password: str 
    num_ideas:int

#for server
class User(BaseModel):
    username: str
    password: str
    num_ideas:int

#for user
class showUser(BaseModel):
    username: str
    num_ideas:int

    class Config:
        from_attributes = True

class input_Ideas(BaseModel):
    startup_idea: str


#for nested data
class Evaluation(BaseModel):
    sentence: str
    score: int


class showIdea(BaseModel):
    startup_idea: str
    creativity: Evaluation
    demand: Evaluation
    uniqueness: Evaluation
    scale: Evaluation
    investment: Evaluation
    
    thinker: showUser

    class Config:
        from_attributes = True