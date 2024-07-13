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




def create_user_handler(item, main_db):
    try:
        logging.info("STARTING SERVICE")
        logging.debug(f"REQUEST: {item.dict()}")
        main_db.update_tables()
        session = main_db.get_session()
        if item.password != item.confirmPassword: 
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
        # Create a new user
        new_user = User(email=item.email, 
                        firstName=item.firstName, 
                        lastName=item.lastName, 
                        phoneNumber=item.phoneNumber, 
                        country=item.country, 
                        username=item.username, 
                        hashed_password=hashed_password, 
                        userType=item.userType)
        logging.debug(f"User to be created: \n\n{new_user.username}")
        session.add(new_user)
        session.commit()
        resp_body = {"status": "success", "username": item.username, "userType": item.userType}
        logging.info(f"User created successfully: \n\n{resp_body}")
        return resp_body
    except IntegrityError as integ_error:
        session.rollback()
        if "already exists" in integ_error._message() and item.username in integ_error._message():
            logging.error(f"User '{item.username}' already registered!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif "already exists" in integ_error._message() and item.email in integ_error._message():
            logging.error(f"User's email '{item.email}' already registered!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif "already exists" in integ_error._message() and item.phoneNumber in integ_error._message():
            logging.error(f"User's phoneNumber '{item.phoneNumber}' already registered!")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            logging.error(f"Internal server error: '{integ_error}'")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
                headers={"WWW-Authenticate": "Bearer"},
            )
