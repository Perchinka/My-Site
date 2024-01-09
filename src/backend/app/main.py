from datetime import timedelta
import uvicorn

from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel
from typing import List

from utils import get_connection
from auth import authenticate_user, create_access_token, get_current_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Tutorials DataClasses
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

# Users DataClasses
class User(BaseModel):
    id: int = None
    username: str
    password: str
    id_role: int # 0 - Admin, 1 - User TODO: Make Enum or something like that
    email: str = None
    verified: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

app = FastAPI(debug=True)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Tutorials
@app.get("/tutorials", response_model=List[Tutorial], 
         status_code=status.HTTP_200_OK, tags=["Tutorials"])
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

@app.post("/tutorials", status_code=status.HTTP_201_CREATED, tags=["Tutorials"])
async def create_post(tutorial: Tutorial):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO tutorials (title, description, visible, thumbnail, url) VALUES (%s, %s, %s, %s, %s)",
                (tutorial.title, tutorial.description, tutorial.visible, tutorial.thumbnail, tutorial.url))
    cur.close()
    
    conn.commit()
    conn.close()

    return

@app.put("/tutorials", tags=["Tutorials"])
async def update_post(tutorial: UpdateTutorialBodyRequest):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE tutorials SET title = %s, description = %s, visible = %s, thumbnail = %s, url = %s WHERE id = %s",
                (tutorial.title, tutorial.description, tutorial.visible, tutorial.thumbnail, tutorial.id, tutorial.url))
    
    cur.close()
    conn.commit()
    conn.close()

    return

@app.put("/tutorials/visibility/{id}", tags=["Tutorials"])
async def update_post_visibility(tutorial_id: str, visibility: bool):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE tutorials SET visible = %s WHERE id = %s",
                (visibility, tutorial_id))
    
    cur.close()
    conn.commit()
    conn.close()

    return

@app.delete("/tutorials/{id}", tags=["Tutorials"])
async def delete_post(tutorial_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tutorials WHERE id = %s", (tutorial_id,))
    
    cur.close()
    conn.commit()
    conn.close()

    return

# Authentification
@app.post("/token", tags=["Authentification"], response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user[1]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", tags=["Authentification"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# TODO: Unique username and email, password hashing
@app.post("/users", tags=["Authentification"])
async def create_new_user(username, password, email):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                    (username, password, email))
        cur.close()
        
        conn.commit()
        conn.close()
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return HTTPException(status_code=status.HTTP_201_CREATED)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)