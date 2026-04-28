from pydantic import BaseModel, Field, field_validator

class ChatRequest(BaseModel):
    userId:  str = Field(default="1", min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message cannot be blank or whitespace only")
        return v.strip()

class EndSessionRequest(BaseModel):
    userId: str = Field(..., min_length=1, max_length=100)
