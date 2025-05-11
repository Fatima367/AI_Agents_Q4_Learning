from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        ..., # means the parameter is required
        title= "ID of the item",
        description="A unique identifier for the item",
        ge= 1 # means greater than or equal to one
    )
):
    return {"item_id": item_id}