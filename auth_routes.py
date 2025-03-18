from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from db_config import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

session = Session(bind=engine)


@auth_router.get('/')
async def home(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Token')
    return {"message": "Hello Auth User [Saurabh] "}


@auth_router.post('/signup')
async def signup(request: SignUpModel):
    existing_user = session.query(User).filter(
        (User.username == request.username) | (User.email == request.email)
    ).first()

    if existing_user:
        if existing_user.email == request.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'User with the email {request.email} already exists.'
            )
        elif existing_user.username == request.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Username {request.username} is already taken, please try again.'
            )
    hash_password = generate_password_hash(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        password=hash_password,
        is_active=request.is_active,
        is_staff=request.is_staff
    )

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # This will fetch the updated user object with the generated ID
    except Exception as e:
        session.rollback()  # Rollback the transaction in case of error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user."
        )
    # To ensure password isn't returned to the response
    new_user.password = None

    # Return a success message with the user details
    return {
        "message": "New user has been created successfully!",
        "user_details": new_user,
        "status_code": status.HTTP_201_CREATED,
    }


@auth_router.post('/login')
async def login(request: LoginModel, Authorize: AuthJWT = Depends()):
    user_exist = session.query(User).filter(User.username == request.username).first()
    if user_exist is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Invalid Username: {request.username}'
        )
    # Check password hash directly
    if not check_password_hash(user_exist.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid Password, please check the entered credentials'
        )

    access_token = Authorize.create_access_token(subject=user_exist.username)
    refresh_token = Authorize.create_refresh_token(subject=user_exist.username)
    response = {
        "token":
            {
                "access": access_token,
                "refresh": refresh_token
            }

    }
    return jsonable_encoder(response)


@auth_router.get('/refresh')
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='please provide valid refresh token')

    current_user = Authorize.get_jwt_subject()
    print("Check Current user name: ", current_user)

    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({
        "access_token": access_token
    })
