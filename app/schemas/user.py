from pydantic import BaseModel, EmailStr,ConfigDict,Field,field_validator
from pathlib import Path

COMMON_PASSWORDS_PATH = Path(__file__).parent / "common_passwords.txt"

def load_common_passwords():
    with open(COMMON_PASSWORDS_PATH, encoding="utf-8") as file:
        return {line.strip().lower() for line in file if line.strip()}

COMMON_PASSWORDS = load_common_passwords()
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(not char.isalnum() for char in value):
            raise ValueError("Password must contain at least one special character")

        if value.lower() in COMMON_PASSWORDS:
            raise ValueError("Password is too common")
        
        return value
class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)