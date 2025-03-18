from pydantic import BaseModel
from typing import Optional
from models import OrderStatusEnum, FoodSizeEnum


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


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = OrderStatusEnum.pending
    food_size: Optional[str] = FoodSizeEnum.small
    user_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 2,
                "food_size": "medium"
            }
        }
