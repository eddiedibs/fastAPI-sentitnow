
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
import jwt
import hashlib
from time import sleep
from sqlalchemy.exc import IntegrityError

from src.data.models import login_credentials_model,signup_credentials_model
from src.data.database import db, users
from src.data import constants as const
from src.utils import common

app = FastAPI()



# Secret key to sign JWT tokens (You should generate a strong, unique secret key for your application)
SECRET_KEY = const.SECRET_KEY
ALGORITHM = const.ALGORITHM

# Sample user data (in a real-world scenario, you would fetch this from a database)
MAIN_DB = db()

# Define OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create a JWT token
def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# # Dependency to get the current user based on the provided JWT token
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except Exception as exp:
#         print("ERROR: ", exp)
#         raise credentials_exception

#     user = get_user(username)
#     if user is None:
#         raise credentials_exception

#     return user

# # Route to get information about the current user
# @app.get("/users/me", response_model=dict)
# async def read_users_me(current_user: dict = Depends(get_current_user)):
#     return current_user

@app.post("/create_user")
async def create_user(item: signup_credentials_model = Body(...)):
    try:
        if item.password != item.confirm_password: 
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords don't match!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        if not common.email_isvalid(item.email):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not valid!",
            headers={"WWW-Authenticate": "Bearer"},
        )
        hashed_password = hashlib.sha256(item.password.encode()).hexdigest()
        ins = users.insert().values(email=item.email, username=item.username, password=hashed_password, grant_type=const.GRANT_TYPE)
        MAIN_DB.update_tables()
        MAIN_DB.get_db().execute(ins)
        return {"username": item.username, "grant_type": const.GRANT_TYPE}

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered!",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Route to authenticate and get a JWT token
@app.post("/token", response_model=dict)
async def login_for_access_token(item: login_credentials_model = Body(...)):
    hashed_password = hashlib.sha256(item.password.encode()).hexdigest()

    # Query the database to check and validate the user
    query = users.select().where(users.c.username == item.username, users.c.password == hashed_password)
    retrieved_user = MAIN_DB.db_query(query)
    user_to_dict = [dict(user) for user in retrieved_user]
    if user_to_dict == []:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": user_to_dict[0]["username"]}
    return {"access_token": create_jwt_token(token_data), "token_type": "bearer"}