from scripts.exception import GenAIException
from scripts.schemas import ReturnSuccessSchema
from scripts.schemas.user_schemas import UpdateProfileSchema
from scripts.utils.mongo_util.user import User
from fastapi import status


class UserHandler:
    def __init__(self):
        self.user_collection = User()

    async def get_user(self, email_id: str):
        """
        Get user details.

        This endpoint allows a user to get their account details.

        Args:
            email_id (str): The email ID of the user.

        Returns:
            ResponseModel: A response model containing the user's details.

        Raises:
            HTTPException: If there is an error getting the user's details.
        """
        user = self.user_collection.find_one({"email": email_id}, filters={"_id": 0})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        return ReturnSuccessSchema(data=user, message="User details retrieved successfully.")

    async def update_user(self,update_payload: UpdateProfileSchema):
        """
        Update user details.

        This endpoint allows a user to update their account details.

        Args:
            update_payload (UpdateProfileSchema): The payload containing the user's updated details.

        Returns:
            ResponseModel: A response model containing the updated user's details.

        Raises:
            HTTPException: If there is an error updating the user's details.
        """
        user = self.user_collection.find_one({"email": update_payload.email}, filters={"_id": 0})
        if not user:
            raise GenAIException("User not found.", code=status.HTTP_404_NOT_FOUND)
        self.user_collection.update_one({"email": update_payload.email}, {"$set": update_payload.model_dump(exclude={"email"})})
        return ReturnSuccessSchema(message="User details updated successfully.")
