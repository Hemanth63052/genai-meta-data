from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str

class SignupSchema(LoginSchema):
    first_name: str
    last_name: str

class ChangePasswordSchema(LoginSchema):
    new_password: str