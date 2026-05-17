from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str