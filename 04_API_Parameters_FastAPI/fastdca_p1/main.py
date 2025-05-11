from fastapi import FastAPI, Path, Query, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float

@app.get("items/{item_id}")
async def read_item(
    item_id: int = Path(
        ..., # means this parameter is required
        title="The ID of the item",
        description="A unique identifier for the item",
        ge = 1
    )
):
    return {"item_id": item_id}


@app.get("/items/")
async def read_items(
    q: str | None = Query(
        None,  # Default value is None (optional parameter)
        title= "Query string",
        description="Query string for searching items",
        min_length = 3,
        max_length = 50
        ),
    # 'skip' is a query parameter used to skip a number of items (e.g., pagination) like if 10 items on each page so skip=10 would show from 11th item on next page
    skip: int = Query(0, ge=0), # Greater than or equal to zero, 

    # 'limit' is a query parameter to limit the number of results returned like if 100 results show 10 by default
    limit: int = Query(10, le=100) # Less than or equal to 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.put("/items/validated/{item_id}")
async def update_item(
    item_id: int = Path(..., title= "Item ID", ge= 1),
    q: str = Query(None, min_length= 3),
    item: Item | None = Body(None, description= "Optional item data (JSON body)")
):
    result = {"item_id": item_id}

    if q:
        result.update({"q": q})
    if item:
        result.update({"item": item.model_dump()})

    return result