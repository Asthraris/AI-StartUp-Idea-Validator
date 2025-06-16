from dotenv import load_dotenv
load_dotenv()


from fastapi import FastAPI
from .routers import authentication,ideas


from . import model
from .database import engine

app = FastAPI()

model.Base.metadata.create_all(engine)

@app.get("/")
def base():
    return {"greet":"hello"}

app.include_router(authentication.router)
app.include_router(ideas.router)