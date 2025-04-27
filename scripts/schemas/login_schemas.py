import uuid

from pydantic import BaseModel, EmailStr, Field, model_validator
from fastapi import status
from typing import Optional
from datetime import datetime, timezone

from scripts.exception import GenAIException


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    @model_validator(mode='before')
    def validate_email(cls, values):
        email = values.get("email")
        if not email:
            raise GenAIException(
                code=status.HTTP_400_BAD_REQUEST,
                message="Email address is required.",
            )
        if not values.get("password"):
            raise GenAIException(
                code=status.HTTP_400_BAD_REQUEST,
                message="Password is required.",
            )
        return values

class SignupSchema(LoginSchema):
    first_name: str
    last_name: str
    user_id: str = Field(default=str(uuid.uuid4()))
    is_active: bool = True
    is_verified: bool = False
    is_deleted: bool = False
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None  # URL if uploaded
    created_at: datetime = Field(default=datetime.now(tz=timezone.utc))
    modified_at: datetime = Field(default=datetime.now(tz=timezone.utc))

    @model_validator(mode='before')
    def validate_password(cls, values):
        if len(values.get("first_name", "")) >= 20 or len(values.get("last_name", "")) >= 20:
            raise GenAIException(
                code=status.HTTP_400_BAD_REQUEST,
                message="First name and last name must be less than 20 characters.",
            )
        password = values.get("password")
        if (not any(c.islower() for c in password)
            or not any(c.isupper() for c in password)
            or not any(c.isdigit() for c in password)
            or not any(c in "!@#$%^&*()" for c in password)
            or len(password) < 8
        ):
            raise GenAIException(
                code=status.HTTP_400_BAD_REQUEST,
                message="Password must meet the following criteria:\n"
                        "- At least one lowercase letter\n"
                        "- At least one uppercase letter\n"
                        "- At least one digit\n"
                        "- At least one special character (@$!%*&)\n"
                        "- Minimum length of 8 characters",
            )
        values['display_name'] = values.get("display_name") or f"{values.get('first_name')} {values.get('last_name')}"
        return values

class ChangePasswordSchema(LoginSchema):
    new_password: str
