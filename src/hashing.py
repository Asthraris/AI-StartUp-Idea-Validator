from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"])

class Hash:
    def bcrypt(plainpswd :str):
        return pwd_cxt.hash(plainpswd)
    def verify(plainpass :str , hashed_pswd: str):
        return pwd_cxt.verify(plainpass, hashed_pswd)
