from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from . import schemas, models
from .database import engine, SessionLocal, Base

from typing import List
from passlib.context import CryptContext

app = FastAPI()

origins = [
    "https://nishithpshetty.gq"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["blog"])
def all(db: Session = Depends(get_db)):
    temp_blogs = db.query(models.Blog).all()
    return temp_blogs

@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["blog"])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    temp_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(temp_blog)
    db.commit()
    db.refresh(temp_blog)
    return temp_blog

@app.delete("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def delete(id: int, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")
    
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body":request.body})
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")
    
@app.post("/user", response_model=schemas.ShowUser, tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    newUser = models.User(name=request.name, email=request.email, password=get_password_hash(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@app.post("/user/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    newUser = db.query(models.User).filter(models.User.id == id).first()
    if newUser:
        return newUser
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

@app.get("/userdel", tags=["user"])
def delete_user(db: Session = Depends(get_db)):
    db.query(models.User).delete()
    db.commit()
    return "OK"