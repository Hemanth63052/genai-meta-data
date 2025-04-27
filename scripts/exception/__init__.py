from fastapi.exceptions import HTTPException
from fastapi import status


class GenAIException(HTTPException):
    def __init__(self, message, code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status = "fail"
        self.code= code
        super().__init__(status_code=self.code, detail=self.message)
