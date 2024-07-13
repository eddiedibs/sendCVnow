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




def send_request(item, authorization, main_db):
    logging.info("STARTING SERVICE")
    logging.debug(f"REQUEST PATH: /send-request/")
    main_db.update_tables()
    session = main_db.get_session()
    token = common.get_token_from_authorization(authorization.credentials)
    token_info = common.decode_token(token)
    if token_info is None:
        logging.error(f"Token info appears None for user")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    if item.username != token_info["sub"]:
        logging.error(f"Not authorized to fetch data")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    db_user = session.query(User).filter(User.username == token_info["sub"]).first()
    if db_user is None:
        logging.error(f"User from DB appears None for username '{token_info['sub']}'")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    ai_resp = common.send_ai_req(req_instruction=item.instruction)

    resp_body = {"id":db_user.id,
            "instruction": item.instruction,
            "ai_response": ai_resp,
            }
    logging.debug(f"AI request sent successfully:  \n\n{resp_body}")
    return resp_body
