from pydantic import BaseModel

class ConversationRequest(BaseModel):
    userId:str
    query:str

class ConversationResponse(BaseModel):
    userId:str
    queryResponse:str

