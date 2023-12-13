from fastapi import FastAPI
from pydantic import BaseModel

class Tutorial(BaseModel):
    title: str
    description: str | None = None
    visible: bool
    image: str | None = None


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/tutorials")
async def create_post(tutorial: Tutorial):
    return tutorial

@app.put("/tutorials/{tutorial_id}")
async def update_post(tutorial_id: str):
    return {"message": f"Tutorial {tutorial_id} has been updated"}

@app.delete("/tutorials/{id}")
async def delete_post(tutorial_id: str):
    return {"message": f"Tutorial {tutorial_id} has been deleted"}
