from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Annotated
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

if not os.path.exists(TASKS_STORAGE_FILE):
    with open(TASKS_STORAGE_FILE, "r") as file:
        tasks = file.read()

def save_tasks(task):
    with open(TASKS_STORAGE_FILE, "w") as file:
        tasks = file.update(task)


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

    def read_user_data(cls, data):
        return data

class Tasks(BaseModel):
    task_id: int
    task_title: str
    tast_content: str
    task_due_date: str

    @validator("task_due_date")
    def is_date_greater_than_today(cls, value):
        if value <= datetime.today():
            return "Due date must not be today or past days"
        
    task = {}

    task[task] = task
    task[task][task_title] = task_title
    task[task][tast_content] = tast_content
    task[task][task_due_date] = task_due_date

    save_tasks(task)
        

@app.post("/users/")
def create_user(user_data = Annotated[dict, Depends(UserCreate)]):
    return UserRead.read_user_data(user_data)
        

@app.get("users/{user_id}")
def get_users(user_id):
    for data in users_data[user_id]:
        if users_data[user_id][password]:
            print("Cannot display password")
            continue
    return users_data[user_id]


@app.post("/tasks/")
def create_user(user_data = Annotated[dict, Depends(Tasks)]):
    return tasks


@app.get("tasks/{task_id}")
def get_users(task_id):
    return tasks[task_id]


@app.put("update//tasks/{task_id}")
def edit_task(task_id):
    