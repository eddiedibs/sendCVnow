
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError, ProgrammingError
import pandas as pd
import logging
import io
from typing import Optional, List
import datetime
import jwt
import hashlib
from time import sleep

from src.data.models import *
from src.data.database import db
from src.data.tables import User
from src.data import constants as const
from src.utils import common
from src.business import *
from src.business import ai_ops

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s|%(funcName)s]:: %(message)s', 
    handlers=[logging.StreamHandler()]
)

app = FastAPI()
token_auth_scheme = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






MAIN_DB = db()

# Define OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Route to authenticate and get a JWT token
@app.post("/token", response_model=dict)
async def login_for_access_token(item: login_credentials_model = Body(...)):
    return token.login_for_access_token_handler(
        item=item,
        main_db=MAIN_DB
        )

@app.post("/create-user")
async def create_user(
        item: signup_credentials_model = Body(...),
        # authorization: HTTPBearer = Depends(token_auth_scheme)
    ):
    return user_creation.create_user_handler(
        item=item,
        main_db=MAIN_DB
        )


# FastAPI path operations
@app.get("/get-user-info/{username}", response_model=dict)
async def get_user_info(
            username: str,
            authorization: HTTPBearer = Depends(token_auth_scheme)
        ):
    return get_user.get_user_info_handler(
        username=username,
        authorization=authorization,
        main_db=MAIN_DB
        )

@app.post("/send-ai-request")
async def send_ai_request(
        item: ai_request_model = Body(...),
        authorization: HTTPBearer = Depends(token_auth_scheme)
    ):
    return ai_ops.send_request(
        item=item,
        authorization=authorization,
        main_db=MAIN_DB
        )



@app.get("/test", response_model=dict)
async def test_setup():
    setUp()
    return {"Test": "Done"}