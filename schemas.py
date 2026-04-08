from pydantic import BaseModel
from typing import Optional, List

class MatchStatus(BaseModel):
    score: str
    batsman: str
    bowler: str
    insight: str
    vibe_score: int

class UserQuery(BaseModel):
    text: str

class AIResponse(BaseModel):
    response: str
    exit: bool = False