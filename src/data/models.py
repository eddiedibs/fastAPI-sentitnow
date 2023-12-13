from pydantic import BaseModel

class login_credentials_model(BaseModel):
   grant_type: str
   username: str
   password: str

class signup_credentials_model(BaseModel):
   email: str
   username: str
   password: str
   confirm_password: str


class error_model(BaseModel):
   httpStatusCode: int
   body: dict
   errors: list