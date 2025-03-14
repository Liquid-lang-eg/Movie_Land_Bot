from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    tg_id: str

class SubscribeRequest(BaseModel):
    user_id: int
    genre_id: int