from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'example',
                'email': 'example@gmail.com',
                'password': 'example@123',
                'is_staff': False,
                'is_active': True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '428d47fa1d8fdffbd174289a2d67130117d8e519427432b9eee18bef1db51b99'


class LoginModel(BaseModel):
    username: str
    password: str

