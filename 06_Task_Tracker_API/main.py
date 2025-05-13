from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
import os

app = FastAPI()

USERS_STORAGE_FILE = "users.py"
users_data = {}

TASKS_STORAGE_FILE = "users.py"
tasks = {}

if not os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        users_data = file.read()

def save_user_data(data):
    with open(USERS_STORAGE_FILE, "w") as file:
        users_data = file.update(data)


class UserCreate(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str

    data = {}

    data[user_id] = user_id
    data[user_id][username] = username
    data[user_id][email] = email
    data[user_id][password] = password.encode().hexidigest()

    save_user_data(data)

class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str

class Tasks(BaseModel):
    task_id: int
    task_title: str
    tast_content: str
    task_due_date: str

    @validator("task_due_date")
    def is_date_greater_than_today(cls, value):
        if value <= datetime.today():
            return "Due date must not be today or past days"
        

@app.get("users/{user_id}")
def get_users()