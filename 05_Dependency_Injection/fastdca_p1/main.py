from fastapi import FastAPI, Depends, Query
from typing import Annotated

app = FastAPI()

# 1. Hello Dependency

def get_simple_goal():
    return {"goal": "We are building AI agents Workforce"}

@app.get("/get-simple-goal")
def simple_goal(response: Annotated[dict, Depends(get_simple_goal)]):
    return response

# 2. Dependency with Parameter
# We can even pass function parameters in Dep.

def get_goal(username: str):
    return {"goal": "We are building AI agents Workforce", "username": username}

@app.get("/get-goal")
def get_my_goal(response: Annotated[dict, Depends(get_goal)]):
    return response


# 3. Dependency with Query Parameters
# Check a Secret Key

# dependency function
def dep_login(username: str = Query(None), password: str = Query(None)):
    if username == "admin" and password == "admin":
        return {"message": "Login Succesful!"}
    else:
        return {"message": "Login Failed"}
    
@app.get("/sigin")
def login_api(user: Annotated[dict, Depends(dep_login)]):
    return user


# 4. Multiple Dependencies
