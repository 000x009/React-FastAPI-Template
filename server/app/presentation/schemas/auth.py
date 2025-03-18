from pydantic import BaseModel, Field, EmailStr


class RegisterSchema(BaseModel):
    email: str
    full_name: str = Field(max_length=50)
