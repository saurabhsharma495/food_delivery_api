from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from auth_routes import auth_router
from order_routes import order_router
from db_config import engine
from schemas import Settings
from initialize_database import check_and_create_table


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    check_and_create_table(engine)


@app.on_event("shutdown")
def shutdown():
    print("Shutting down the FastAPI server...")


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(order_router)
