from fastapi import Depends

from scripts.handlers.user import UserHandler
from scripts.schemas.user_schemas import UpdateProfileSchema
from scripts.services import user_router
from adapt_iq_common.utils.authorization_util import Email


@user_router.get("/profile", tags=["User"])
async def get_user_profile(email: str = Depends(Email())):
    """
    Get user profile.

    This endpoint allows a user to get their profile details.

    Args:
        email (Email): The email of the user.

    Returns:
        dict: A dictionary containing the user's profile details.
    """
    return await UserHandler().get_user(email_id=email)

@user_router.post("/update-profile", tags=["User"])
async def update_user_profile(update_payload: UpdateProfileSchema, email: str = Depends(Email())):
    """
    Update user profile.

    This endpoint allows a user to update their profile details.

    Args:
        email (Email): The email of the user.
        update_payload (UpdateProfileSchema): The payload containing the user's updated details.

    Returns:
        dict: A dictionary containing the updated user's profile details.
    """
    if not update_payload.email:
        update_payload.email = email
    return await UserHandler().update_user(update_payload=update_payload)
