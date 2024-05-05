from pydantic_settings import BaseSettings
import os



class AuthConfig(BaseSettings):
    JWT_ALG: str 
    JWT_SECRET: str 
    JWT_EXP: int = 10080



JWT_ALG = os.getenv("JWT_ALG")
JWT_SECRET = os.getenv("JWT_SECRET")
auth_config = AuthConfig(JWT_ALG=JWT_ALG, JWT_SECRET=JWT_SECRET)
