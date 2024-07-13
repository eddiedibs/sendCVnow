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




def get_user_info_handler(username, authorization, main_db):
    logging.info("STARTING SERVICE")
    logging.debug(f"REQUEST PATH: /get-user-info/{username}")
    main_db.update_tables()
    session = main_db.get_session()
    token = common.get_token_from_authorization(authorization.credentials)
    token_info = common.decode_token(token)
    if token_info is None:
        logging.error(f"Token info appears None for user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    if username != token_info["sub"]:
        logging.error(f"Not authorized to fetch data")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    db_user = session.query(User).filter(User.username == token_info["sub"]).first()
    if db_user is None:
        logging.error(f"User from DB appears None for username '{token_info['sub']}'")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    resp_body = {"id":db_user.id,
            "firstName": db_user.firstName,
            "lastName": db_user.lastName,
            "username": db_user.username,
            "country": db_user.country,
            "phoneNumber": db_user.phoneNumber,
            "email": db_user.email,
            "userType": db_user.userType,
            "session": db_user.session,
            "isActive": db_user.isActive,
            }
    logging.debug(f"User info retrieved successfully:  \n\n{resp_body}")
    return resp_body
