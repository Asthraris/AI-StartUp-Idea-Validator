from fastapi import APIRouter , status , HTTPException ,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import  model ,schema
from typing import List


#AI stuff
from openai import OpenAI, RateLimitError,APIError
from dotenv import load_dotenv
import os
import json

from ..oauth2 import get_current_user



router = APIRouter(prefix="/ideas" , tags=["ideas"])

#loading env data inside the function
OpenAI_key = os.getenv("OPENAI_KEY")


client = OpenAI(api_key= OpenAI_key )


@router.post("", status_code=status.HTTP_201_CREATED)
def publish_idea(
    request: schema.input_Ideas,
    db: Session = Depends(get_db),
    curr_user: schema.baseUser = Depends(get_current_user)
):
    #abhi ke liye isse band rakhte hai bcoz there is not num_ideas in token_data its only usid
    # #limit check
    # if(curr_user.num_ideas > 3):
    #     return {"Uses Exceeded" : curr_user}
    # #uses increment
    # curr_user.num_ideas += 1
    prompt :str = """You are an AI startup evaluator.

    Analyze the following startup idea in terms of:
    - Creativity
    - Demand
    - Uniqueness
    - Scale
    - Investment

    For each of these 5 categories, provide:
    1. A short 1-line analysis sentence.
    2. A score between 1 to 10.

    Return the result in **JSON format** like this:

    {
      "startup_idea": "<your idea here>",
      "evaluation": {
        "creativity": {
          "sentence": "...",
          "score": ...
        },
       "demand": {
          "sentence": "...",
          "score": ...
        },
        "uniqueness": {
          "sentence": "...",
          "score": ...
       },
       "scale": {
         "sentence": "...",
         "score": ...
       },
       "investment": {
         "sentence": "...",
         "score": ...
       }
     }
    }

     Start-up idea:
    """
    prompt += request.startup_idea

    #getting data
    try:
        ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    except json.JSONDecodeError:
        raise HTTPException(status_code=428, detail="AI response was not in JSON format.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI quota exceeded.")
    except APIError as e:
        raise HTTPException(status_code=500, detail="AI service failed: " + str(e))
    #convert it into db storable data
    json_data = json.loads(ai_response.choices[0].message.content)
    #set idea to store in my db
    new_idea = model.Idea(
    startup_idea = json_data["startup_idea"],

    # Evaluation fields
    creativity_sentence = json_data["evaluation"]["creativity"]["sentence"],
    creativity_score    = json_data["evaluation"]["creativity"]["score"],

    demand_sentence     = json_data["evaluation"]["demand"]["sentence"],
    demand_score        = json_data["evaluation"]["demand"]["score"],

    uniqueness_sentence = json_data["evaluation"]["uniqueness"]["sentence"],
    uniqueness_score    = json_data["evaluation"]["uniqueness"]["score"],

    scale_sentence      = json_data["evaluation"]["scale"]["sentence"],
    scale_score         = json_data["evaluation"]["scale"]["score"],

    investment_sentence = json_data["evaluation"]["investment"]["sentence"],
    investment_score    = json_data["evaluation"]["investment"]["score"],

    user_id = curr_user.usid  # assuming `curr_user` is your authenticated user
)

    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)

    return json_data

@router.get("/history",status_code=status.HTTP_200_OK, response_model= List[schema.showIdea])
def get_all(db: Session = Depends(get_db),curr_user: schema.baseUser = Depends(get_current_user)):
    ideas = db.query(model.Idea).filter(model.Idea.user_id == curr_user.usid).all()
    return ideas
