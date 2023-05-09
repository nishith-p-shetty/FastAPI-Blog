from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = None

app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": "Published Blog List",
                "limit": limit}
    else:
        return {"data": "Unpublished Blog List",
                "limit": limit}

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f"Blog is created as {request}"}

@app.get('/blog/unpublished')
def unpublished():
    return {"data": "all unpublished blogs"}

@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}

@app.get("/blog/{id}/comments")
def comments(id: int):
    return {"ID": id,
            "data": {"Comment 1", "Commnet 2"}}