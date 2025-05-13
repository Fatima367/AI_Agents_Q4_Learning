from fastapi import FastAPI, Depends
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