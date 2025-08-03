from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, schema
from typing import List

# AI stuff
import google.genai as genai


from dotenv import load_dotenv
import os
import json

from ..oauth2 import get_current_user

router = APIRouter(prefix="/ideas", tags=["ideas"])




@router.post("", status_code=status.HTTP_201_CREATED)
def publish_idea(
    request: schema.input_Ideas,
    db: Session = Depends(get_db),
    curr_user: schema.baseUser = Depends(get_current_user),
):
    # abhi ke liye isse band rakhte hai bcoz there is not num_ideas in token_data its only usid
    # #limit check
    # if(curr_user.num_ideas > 3):
    #     return {"Uses Exceeded" : curr_user}
    # #uses increment
    # curr_user.num_ideas += 1
    prompt: str = """You are an AI startup evaluator.

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
      "startup_idea": "<idea here>",
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

    # Create the client object once, at the start of your application or within the function if needed
    client = genai.Client()

    try:
      ai_response = client.models.generate_content(
        model="gemini-1.5-flash",  # Pass the model name here
        contents= prompt,          # The new parameter name for the prompt is 'contents'
        
      )
      
    except Exception as e:
      raise HTTPException(status_code=500, detail=f"Gemini API call failed: {e}")

    # Convert it into db storable data
    try:
        # We need to remove the leading "```json\n" and trailing "```"
      raw_json_string = ai_response.text.strip()
      if raw_json_string.startswith("```json"):
        raw_json_string = raw_json_string.removeprefix("```json").removesuffix("```")
      json_data = json.loads(raw_json_string)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=428, detail={"res":"AI response was not in JSON format:",
                                     "out":raw_json_string}
        )
        

    # set idea to store in my db
    new_idea = model.Idea(
        startup_idea=json_data["startup_idea"],
        # Evaluation fields
        creativity_sentence=json_data["evaluation"]["creativity"]["sentence"],
        creativity_score=json_data["evaluation"]["creativity"]["score"],
        demand_sentence=json_data["evaluation"]["demand"]["sentence"],
        demand_score=json_data["evaluation"]["demand"]["score"],
        uniqueness_sentence=json_data["evaluation"]["uniqueness"]["sentence"],
        uniqueness_score=json_data["evaluation"]["uniqueness"]["score"],
        scale_sentence=json_data["evaluation"]["scale"]["sentence"],
        scale_score=json_data["evaluation"]["scale"]["score"],
        investment_sentence=json_data["evaluation"]["investment"]["sentence"],
        investment_score=json_data["evaluation"]["investment"]["score"],
        user_id=curr_user.usid,  # assuming `curr_user` is your authenticated user
    )

    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)

    return json_data


@router.get(
    "/history", status_code=status.HTTP_200_OK, response_model=List[schema.showIdea]
)
def get_all(
    db: Session = Depends(get_db), curr_user: schema.baseUser = Depends(get_current_user)
):
    ideas = (
        db.query(model.Idea).filter(model.Idea.user_id == curr_user.usid).all()
    )
    return ideas