import logging
import hashlib
import datetime

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, ProgrammingError
from src.data.tables import User
from src.utils import common
from src.data.tables import User

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s|%(funcName)s]:: %(message)s', 
    handlers=[logging.StreamHandler()]
)




def login_for_access_token_handler(item, main_db):
    try:
        logging.info("STARTING SERVICE")
        logging.info(f"REQUEST: {item.dict()}")
        main_db.update_tables()
        session = main_db.get_session()
        hashed_password = hashlib.sha256(item.password.encode()).hexdigest()
        # Query the database to check and validate the user
        user = session.query(User).filter(User.username == item.username, User.hashed_password == hashed_password, User.userType == item.userType).first()
        if user == None:
            logging.error(f"User '{item.username}' returned None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No such user or password mismatch",
                headers={"WWW-Authenticate": "Bearer"},
            )
        now_time = datetime.datetime.now()
        time_delta = datetime.timedelta(minutes=8)
        exp_time = now_time + time_delta
        token_data = {"userId":user.id,
                    "sub": user.username,
                    "email": user.email,
                    "country": user.country,
                    "iat": now_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "exp": exp_time.strftime("%Y/%m/%d %H:%M:%S"),
                    "userType": user.userType}

        logging.info(f"Token has been generated for user '{user.username}'")
        return {"access_token": common.create_jwt_token(token_data), "token_type": "bearer"}
    except ProgrammingError:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User table is non-existant",
                headers={"WWW-Authenticate": "Bearer"},
            )
