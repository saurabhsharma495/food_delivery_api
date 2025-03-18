from db_config import Base
from sqlalchemy import Column, Integer, Boolean, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import CheckConstraint


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f'<User {self.username} >'


# Define the Enum for the order status
class OrderStatusEnum(enum.Enum):
    pending = "pending"
    in_transit = "in-transit"
    delivered = "delivered"


# Define the Enum for the order status
class FoodSizeEnum(enum.Enum):
    small = "small"
    medium = "medium"
    large = "large"
    extra_large = "extra_large"


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    order_status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending)
    food_size = Column(Enum(FoodSizeEnum), default=FoodSizeEnum.small)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')

    __table_args__ = (
        CheckConstraint("food_size IN ('small', 'medium', 'large', 'extra_large')", name="food_size_check"),
    )

    def __repr__(self):
        return f'<Order {self.id} >'
