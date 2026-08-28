from pydantic import BaseModel


class UserMessage(BaseModel):
    message: str


class AIResponse(BaseModel):
    response: str
