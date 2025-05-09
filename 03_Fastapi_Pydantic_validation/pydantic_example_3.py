from pydantic import BaseModel, EmailStr, validator, ValidationError, field_validator
from typing import List

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: List[Address]


    # @validator("name") Old (Pydantic v1)      The function "validator" is deprecated.
    # @field_validator("name")        # New (Pydantic v2) – Recommended
    # @classmethod

    
    @validator("name")
    def name_must_be_atleast_two_chars(cls, value):
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return value
    
    
# Testing with invalid data
try:
    invalid_user = UserWithAddress(
        id=3,
        name="A",  # single letter only
        email="charlie@example.com",
        address=[{"street": "789 Pine Rd", "city": "Chicago", "zip_code": "60601"}],
    )
except ValidationError as e:
    print(e)