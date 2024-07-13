import logging
import hashlib
import datetime
import os
import shutil
import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, ProgrammingError
from src.data.tables import User
from src.utils import common
from src.data.tables import User
from src.data import constants as const

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s|%(funcName)s]:: %(message)s', 
    handlers=[logging.StreamHandler()]
)




def import_cv_data(file, authorization, main_db):
    logging.info("STARTING SERVICE")
    logging.debug(f"REQUEST FILE: {file.filename}")
    main_db.update_tables()
    session = main_db.get_session()
    token = common.get_token_from_authorization(authorization.credentials)
    token_info = common.decode_token(token)
    if token_info is None:
        logging.error(f"Token info appears None for user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    db_user = session.query(User).filter(User.username == token_info["sub"]).first()
    cv_name_id = db_user.username + "-" +file.filename.split(".pdf")[0] + "-" + str(uuid.uuid4())
    db_user.cv_name_id = cv_name_id
    session.commit()

    # Define the base directory for CVs
    cv_dir = os.path.join(const.BASE_DIR, "CVs")

    # Check if the directory exists, if not, create it
    if not os.path.exists(cv_dir):
        os.makedirs(cv_dir)

    return cv_dir, cv_name_id
    # logging.info(f"Data has been saved successfully: \n\n{resp_body}")
    # return resp_body