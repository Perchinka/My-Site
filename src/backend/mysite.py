import uvicorn
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
    url: str = None

class UpdateTutorialBodyRequest(BaseModel):
    id: int
    title: str
    description: str
    visible: bool
    thumbnail: str
    url: str


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
            "thumbnail": row[4],
            "url": row[5]
        })
    cur.close()
    conn.close()

    return formated_posts

@app.post("/tutorials", status_code=status.HTTP_201_CREATED)
async def create_post(tutorial: Tutorial):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO tutorials (title, description, visible, thumbnail) VALUES (%s, %s, %s, %s, %s)",
                (tutorial.title, tutorial.description, tutorial.visible, tutorial.thumbnail, tutorial.url))
    cur.close()
    
    conn.commit()
    conn.close()

    return

@app.put("/tutorials/")
async def update_post(tutorial: UpdateTutorialBodyRequest):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE tutorials SET title = %s, description = %s, visible = %s, thumbnail = %s, url = %s WHERE id = %s",
                (tutorial.title, tutorial.description, tutorial.visible, tutorial.thumbnail, tutorial.id, tutorial.url))
    
    cur.close()
    conn.commit()
    conn.close()

    return

@app.put("/tutorials/visibility/{id}")
async def update_post_visibility(tutorial_id: str, visibility: bool):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE tutorials SET visible = %s WHERE id = %s",
                (visibility, tutorial_id))
    
    cur.close()
    conn.commit()
    conn.close()

    return

@app.delete("/tutorials/{id}")
async def delete_post(tutorial_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tutorials WHERE id = %s", (tutorial_id,))
    
    cur.close()
    conn.commit()
    conn.close()

    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)