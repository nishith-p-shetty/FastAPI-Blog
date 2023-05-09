from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/blog")
def all(db: Session = Depends(get_db)):
    temp_blogs = db.query(models.Blog).all()
    return temp_blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    temp_blog = models.Blog(title=request.title, body=request.body)
    db.add(temp_blog)
    db.commit()
    db.refresh(temp_blog)
    return temp_blog

@app.delete("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete(id: int, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")
    
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body":request.body})
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")