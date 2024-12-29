from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# print(f"Hashed password:{hash_password("12345")}")
print(f"result: {verify_password("12345","$2b$12$/T66hHyTHJCO56oPFAkbpuSMcEhLb7HNJkNapNZPpNuuo2Gl4d2XG")}")