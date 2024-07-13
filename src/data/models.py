from pydantic import BaseModel

class login_credentials_model(BaseModel):
   username: str
   password: str
   userType: str

# class get_user_info(BaseModel):
#    username: str
#    password: str

class signup_credentials_model(BaseModel):
   firstName: str
   lastName: str
   phoneNumber: str
   country: str
   email: str
   username: str
   password: str
   confirmPassword: str
   userType: str

class ai_request_model(BaseModel):
   username: str
   aiModel: str
   instruction: str

# class upload_cv_model(BaseModel):
#    username: str
#    cvNameId: str

class error_model(BaseModel):
   httpStatusCode: int
   body: dict
   errors: list