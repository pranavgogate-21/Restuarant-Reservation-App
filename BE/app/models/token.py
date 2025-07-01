from pydantic import BaseModel

class TokenOut(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None

    class Config:
        from_attributes = True