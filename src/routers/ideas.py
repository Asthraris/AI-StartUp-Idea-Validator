from fastapi import APIRouter , status , HTTPException ,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import  model ,schema
from typing import List

from ..oauth2 import get_current_user
router = APIRouter(prefix="/ideas" , tags=["ideas"])

@router.post("", status_code=status.HTTP_201_CREATED)
def publish_idea(
    request: schema.Ideas,
    db: Session = Depends(get_db),
    curr_user: schema.baseUser = Depends(get_current_user)
):
    new_idea = model.Ideas(
        content=request.content,
        user_id=curr_user.usid  # Use user_id for FK
    )
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return {"detail": "Published", "idea_id": new_idea.id}

@router.get("/history",status_code=status.HTTP_200_OK, response_model= List[schema.showIdeas])
def get_all(db: Session = Depends(get_db),curr_user: schema.baseUser = Depends(get_current_user)):
    ideas = db.query(model.Ideas).filter(model.Ideas.user_id == curr_user.usid).all()
    return ideas

