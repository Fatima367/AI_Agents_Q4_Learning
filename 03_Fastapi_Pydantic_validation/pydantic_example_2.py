from pydantic import BaseModel, EmailStr

# Defining a nested model
class Address(BaseModel):
    street: str
    city: str
    zip_code: str

# Defining a simple model
class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr # built in validator for email format
    address: list[Address] # list of nested address models


# Valid user data with nested structure
userdata = {"id": 2, 
            "name": "Alice", 
            "email": "alice@example.com", 
            "address": [
                {"street": "123 Main st", "city": "NY", "zip_code":"38746"},
                {"street": "e38 old st", "city": "Houston", "zip_code":"27339"}
            ]
            }

user = UserWithAddress.model_validate(userdata) # create and validate a model instance from raw data (usually a dict or JSON-like input)
print(user.model_dump()) # converts the Pydantic model instance back into a dictionary