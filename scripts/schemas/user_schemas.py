from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


class UpdateProfileSchema(BaseModel):
    """
    Schema for updating user profile.

    Attributes:
        email (str): The email ID of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        display_name (str): The display name of the user.
        profile_picture (str): The URL of the user's profile picture.
    """

    email: Optional[EmailStr] = None
    first_name: str
    last_name: str
    display_name: Optional[str] = None
    profile_picture: str = Field(default=None)
    modified_at: datetime = Field(default=datetime.now(tz=timezone.utc))

    @model_validator(mode='before')
    def validate_display_name(cls, values):
        values['display_name'] = values.get("display_name") or f"{values.get('first_name')} {values.get('last_name')}"
        return values
