from pydantic import BaseModel

class UserSchema(BaseModel):
    tg_id: int

    class Config:
        orm_mode = True

class SubscribeRequest(BaseModel):
    user_id: int
    genre_id: int