import uvicorn
import psycopg2
from fastapi import FastAPI, status

from pydantic import BaseModel
from typing import List

from utils import get_connection

class Tutorial(BaseModel):
    id: int = None
    title: str
    description: str = None
    visible: bool
    thumbnail: str = None


app = FastAPI(debug=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tutorials", response_model=List[Tutorial], status_code=status.HTTP_200_OK)
async def get_tutorials():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tutorials ORDER BY id DESC")
    rows = cur.fetchall()

    formated_posts = []
    for row in rows:
        formated_posts.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "visible": row[3],
            "thumbnail": row[4]
        })
    cur.close()
    conn.close()

    return formated_posts

@app.post("/tutorials", status_code=status.HTTP_201_CREATED)
async def create_post(tutorial: Tutorial):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO tutorials (title, description, visible, thumbnail) VALUES (%s, %s, %s, %s)",
                (tutorial.title, tutorial.description, tutorial.visible, tutorial.thumbnail))
    cur.close()
    
    conn.commit()
    conn.close()

    return

@app.put("/tutorials/{tutorial_id}")
async def update_post(tutorial_id: str):
    return {"message": f"Tutorial {tutorial_id} has been updated"}

@app.delete("/tutorials/{id}")
async def delete_post(tutorial_id: str):
    return {"message": f"Tutorial {tutorial_id} has been deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)