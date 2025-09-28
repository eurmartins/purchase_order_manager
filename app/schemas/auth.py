from pydantic import BaseModel


class JWTSchemas:
    class Token(BaseModel):
        access_token: str
        token_type: str

    class TokenData(BaseModel):
        username: str | None = None

    class UserLogin(BaseModel):
        username: str
        password: str
