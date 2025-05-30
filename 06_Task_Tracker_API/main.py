from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime, date
from typing import Annotated
import json
import os

USER_NOT_FOUND_MSG = "User not found"

app = FastAPI()

USERS_STORAGE_FILE = "users.json"
TASKS_STORAGE_FILE = "tasks.json"


users_data = {}
tasks_data = {}

if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as file:
        users_data = json.load(file)


if os.path.exists(TASKS_STORAGE_FILE):
    with open(TASKS_STORAGE_FILE, "r") as file:
        tasks_data = json.load(file)


def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as file:
        json.dump(users_data, file, indent=4)


def save_tasks():
    with open(TASKS_STORAGE_FILE, "w") as file:
        json.dump(tasks_data, file, indent=4)


class UserCreate(BaseModel):
    user_id: int
    username: constr(min_length= 3, max_length= 20)
    email: EmailStr
    password: str

class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class Tasks(BaseModel):
    task_id: int
    user_id: int
    task_title: str
    task_content: str
    task_due_date: date
    status: str = "pending"

    @validator("task_due_date")
    def is_date_greater_than_today(cls, value):
        if value <= date.today():
            return "Due date must be in the future"
        
        return value
    
    @validator("status")
    def validate_status(cls, value):
        if value not in ["pending", "in_progress", "completed"]:
            return ValueError("Invalid status. Must be 'pending', 'in_progress', or 'completed'")
        
        return value
  

@app.post("/users/", response_model = UserRead)
def create_user(user: UserCreate):

    if user.user_id in users_data:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_data[user.user_id] = user.dict()

    save_user_data()
    return UserRead(**user.dict())
        

@app.get("/users/{user_id}", response_model= UserRead)
def get_users(user_id: int):
    
    user = users_data.get(user_id)

    if not user:
        raise HTTPException(status_code= 404, detail= USER_NOT_FOUND_MSG)
    
    return UserRead(**user)


@app.post("/tasks/", response_model= Tasks)
def create_task(task: Tasks):

    if task.task_id in tasks_data:
        raise HTTPException(status_code=400, detail="Task already exists")
    
    if task.user_id not in users_data:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MSG)
    
    tasks_data[task.task_id] = task.dict() 

    save_tasks()
    return task



@app.get("/tasks/{task_id}", response_model= Tasks)
def get_tasks(task_id: int):
    
    task = tasks_data.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task


@app.put("/tasks/{task_id}", response_model = Tasks)
def update_task_status(task_id: int, status: str):
    
    task = tasks_data.get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if status not in ["pending", "in_progress", "completed"]:
        raise HTTPException(status_code = 400, detail= "Invalid status value")
    
    task["status"] = status

    tasks_data[task_id] = task

    save_tasks()

    return task


@app.get("/users/{user_id}/tasks", response_model= list(Tasks))
def get_user_tasks(user_id: int):
    
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MSG)
    
    return [Tasks(**t) for t in tasks_data.values() if t["user_id"] == user_id]