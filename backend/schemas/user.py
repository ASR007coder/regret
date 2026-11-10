# backend/schemas/user.py

from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupUser(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    dob: date 

    phone: str = Field(
        max_length=15
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower()

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value):
        return value.strip()


class SignupResponse(BaseModel):
    
    user_id: int
    name: str
    email: EmailStr
    is_verified: bool
    message: str

class LoginUser(BaseModel):
    
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.strip().lower()

class LoginResponse(BaseModel):
    
    user_id: int
    name: str
    email: EmailStr

    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    message: str

from pydantic import ConfigDict


class MeResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    name: str
    dob: date
    phone: str
    email: EmailStr
    is_verified: bool