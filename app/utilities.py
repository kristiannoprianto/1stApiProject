from passlib.context import CryptContext

hashing_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return hashing_pwd.hash(password)

def verify(plain_pwd: str, hashed_pwd: str):
    return hashing_pwd.verify(plain_pwd, hashed_pwd)