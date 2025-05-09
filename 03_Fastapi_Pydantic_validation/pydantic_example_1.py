from pydantic import BaseModel, ValidationError

# Defining a simple model
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None # Optional field with default value


# Valid user data
userdata = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 17}
user = User(**userdata)
print(user)
print(user.model_dump())


# Invalid user data
try:
    invalid_user = User(id="not_an_int", name= "BOB", email="bob@example.com")
except ValidationError as e:
    print(e)