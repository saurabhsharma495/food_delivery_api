from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from schemas import OrderModel
from db_config import Session, engine
from models import User, Order

order_router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)

session = Session(bind=engine)


@order_router.get('/')
async def home(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    return {"message": "Saurabh order's"}


@order_router.post('/order')
async def create_order(request: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)

    user = session.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    order_place = Order(
        quantity=request.quantity,
        food_size=request.food_size,
        user=user
    )
    try:
        session.add(order_place)
        session.commit()
        session.refresh(order_place)
    except Exception as e:
        session.rollback()  # Rollback the order in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the order: {str(e)}"
        )
    # Return a success message with the user details
    return {
        "message": "Order has been successfully places!",
        "order_details": order_place,
        "status_code": status.HTTP_201_CREATED
    }


@order_router.get('/order')
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    if not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have access to see all the orders.")
    orders = session.query(Order).all()

    return {
        "message": "All orders",
        "orders_list": orders,
        "status_code": status.HTTP_200_OK
    }


@order_router.get('/order/{id}')
async def get_order_info(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    order_details = session.query(Order).filter(Order.id == id).first()
    if not order_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"order details not found for order id: {id}")

    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have access to see the orders details")
    return {
        "message": f"order details of Id: {id}",
        "order_details": order_details,
        "status_code": status.HTTP_200_OK
    }


@order_router.get('/user/orders')
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    user_orders = user.orders
    return {
        "message": f"all orders of {current_user} user",
        "user_orders": user_orders,
        "status_code": status.HTTP_200_OK
    }


@order_router.get('/user/orders/{id}')
async def get_user_orders(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    # Fetch the order for the specific user by order ID
    user_order = session.query(Order).filter(Order.id == id, Order.user_id == user.id).first()

    if not user_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Order details not found for order id: {id} and username: {current_user}")

    return {
        "message": f"Order details for user id: {id}",
        "user_details": user_order,  # Order is directly returned and automatically serialized by Pydantic
        "status_code": status.HTTP_200_OK
    }


