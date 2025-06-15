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

#for server
class User(BaseModel):
    username: str
    password: str

#for user
class showUser(BaseModel):
    username: str

    class Config:
        from_attributes = True

class Ideas(BaseModel):
    content: str


class showIdeas(BaseModel):
    content: str
    thinker: showUser  # expects relationship in ORM

    class Config:
        from_attributes = True