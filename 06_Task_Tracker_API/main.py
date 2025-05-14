# from fastapi import FastAPI, Depends
# from pydantic import BaseModel, EmailStr, constr
# from datetime import datetime
# from typing import Annotated
# import os

# app = FastAPI()

# USERS_STORAGE_FILE = "users.py"
# users_data = {}

# TASKS_STORAGE_FILE = "users.py"
# tasks = {}

# if not os.path.exists(USERS_STORAGE_FILE):
#     with open(USERS_STORAGE_FILE, "r") as file:
#         users_data = file.read()

# def save_user_data(data):
#     with open(USERS_STORAGE_FILE, "w") as file:
#         users_data = file.update(data)

# if not os.path.exists(TASKS_STORAGE_FILE):
#     with open(TASKS_STORAGE_FILE, "r") as file:
#         tasks = file.read()

# def save_tasks(task):
#     with open(TASKS_STORAGE_FILE, "w") as file:
#         tasks = file.update(task)


# class UserCreate(BaseModel):
#     user_id: int
#     username: str
#     email: EmailStr
#     password: str

#     data = {}

#     data[user_id] = user_id
#     data[user_id][username] = username
#     data[user_id][email] = email
#     data[user_id][password] = password.encode().hexidigest()

#     save_user_data(data)

# class UserRead(BaseModel):
#     user_id: int
#     username: str
#     email: EmailStr
#     password: str

#     def read_user_data(cls, data):
#         return data

# class Tasks(BaseModel):
#     task_id: int
#     task_title: str
#     tast_content: str
#     task_due_date: str

#     @validator("task_due_date")
#     def is_date_greater_than_today(cls, value):
#         if value <= datetime.today():
#             return "Due date must not be today or past days"
        
#     task = {}

#     task[task] = task
#     task[task][task_title] = task_title
#     task[task][tast_content] = tast_content
#     task[task][task_due_date] = task_due_date

#     save_tasks(task)
        

# @app.post("/users/")
# def create_user(user_data = Annotated[dict, Depends(UserCreate)]):
#     return UserRead.read_user_data(user_data)
        

# @app.get("users/{user_id}")
# def get_users(user_id):
#     for data in users_data[user_id]:
#         if users_data[user_id][password]:
#             print("Cannot display password")
#             continue
#     return users_data[user_id]


# @app.post("/tasks/")
# def create_user(user_data = Annotated[dict, Depends(Tasks)]):
#     return tasks


# @app.get("tasks/{task_id}")
# def get_users(task_id):
#     return tasks[task_id]


# @app.put("update//tasks/{task_id}")
# def edit_task(task_id):
#     pass



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime, date
from typing import Dict, List
import json
import os

app = FastAPI()

# File paths
USERS_STORAGE_FILE = "users.json"
TASKS_STORAGE_FILE = "tasks.json"

# In-memory stores
users_data: Dict[int, dict] = {}
tasks_data: Dict[int, dict] = {}

# Load data from files if they exist
if os.path.exists(USERS_STORAGE_FILE):
    with open(USERS_STORAGE_FILE, "r") as f:
        users_data = json.load(f)

if os.path.exists(TASKS_STORAGE_FILE):
    with open(TASKS_STORAGE_FILE, "r") as f:
        tasks_data = json.load(f)

# Save data to files
def save_user_data():
    with open(USERS_STORAGE_FILE, "w") as f:
        json.dump(users_data, f, indent=4)

def save_task_data():
    with open(TASKS_STORAGE_FILE, "w") as f:
        json.dump(tasks_data, f, indent=4)

# Models
class UserCreate(BaseModel):
    user_id: int
    username: constr(min_length=3, max_length=20)
    email: EmailStr
    password: str

class UserRead(BaseModel):
    user_id: int
    username: str
    email: EmailStr

class Task(BaseModel):
    task_id: int
    user_id: int
    task_title: str
    task_content: str
    task_due_date: date
    status: str = "pending"

    @validator("task_due_date")
    def due_date_must_be_in_future(cls, value):
        if value <= date.today():
            raise ValueError("Due date must be in the future")
        return value

    @validator("status")
    def validate_status(cls, value):
        if value not in ["pending", "in_progress", "completed"]:
            raise ValueError("Invalid status. Must be 'pending', 'in_progress', or 'completed'")
        return value

# Endpoints

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    if user.user_id in users_data:
        raise HTTPException(status_code=400, detail="User already exists")
    users_data[user.user_id] = user.dict()
    save_user_data()
    return UserRead(**user.dict())

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = users_data.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(**user)

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    if task.task_id in tasks_data:
        raise HTTPException(status_code=400, detail="Task already exists")
    if task.user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
    tasks_data[task.task_id] = task.dict()
    save_task_data()
    return task

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks_data.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: int, status: str):
    task = tasks_data.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if status not in ["pending", "in_progress", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status value")
    task["status"] = status
    tasks_data[task_id] = task
    save_task_data()
    return task

@app.get("/users/{user_id}/tasks", response_model=List[Task])
def get_tasks_for_user(user_id: int):
    if user_id not in users_data:
        raise HTTPException(status_code=404, detail="User not found")
    return [Task(**t) for t in tasks_data.values() if t["user_id"] == user_id]
