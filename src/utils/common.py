import jwt
import base64
import json
import re
import datetime
from src.data import constants as const
from ollama import Client
import sys




def email_isvalid(email):   
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  
    if(re.search(regex,email)):   
        # print("Valid Email")   
        return True

    else:   
        # print("Invalid Email") 
        return False

def get_token_from_authorization(authorization: str) -> str:
    return authorization.replace('bearer ', '').replace('Bearer ', '')
# Function to create a JWT token
def create_jwt_token(data: dict):
    return jwt.encode(data, const.SECRET_KEY, algorithm=const.ALGORITHM)

def decode_token(token):
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    now_time = datetime.datetime.now()
    end_time = datetime.datetime.strptime(decoded_token["exp"], "%Y/%m/%d %H:%M:%S")
    if now_time > end_time:
        return None
    else:
        return decoded_token

def get_user_info_from_token(token):
    return json.loads(base64.b64decode(token))

def format_amount(n):
    if type(n) == float or type(n)== int:
        return "{:,.0f}".format(n).replace(',','.')
    else:
        return "{:,.0f}".format(float(n)).replace(',', '.')

def send_confirmation_email():  
    fm = FastMail(conf)
    message = MessageSchema(
        subject='Confirm your email',
        recipients=['user@example.com'], # List of recipients, as many as you can pass 
        body='Please click the following link to confirm your email',
        template_body = {
            'first_name': 'User',
            'confirmation_link': 'http://localhost:8000/confirm?token=' + token
        }
    )
    fm.send_message(message)

def send_ai_req(req_instruction):
    client = Client(host=f"{const.OLLAMA_HOST}:{const.OLLAMA_PORT}")
    msgs = [{"role": "system", "content": const.OLLAMA_INIT_INSTRUCT},
            
            {"role": "user", "content": req_instruction}]
    output = client.chat(model="llama3:instruct", messages=msgs, stream=False)

    # for chunk in output:
    #     content = chunk['message']['content']
    #     print(content, end='', flush=True)
    return output