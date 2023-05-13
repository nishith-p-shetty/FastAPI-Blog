from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

from typing import List

from .. import crud

from . import oauth2

from .. import schemas, models, database

router = APIRouter(
    tags=["Blog"],
    prefix="/blog"
)

@router.get("/", response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(database.get_db)):
    return crud.get_all(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id: int, response: Response, db: Session = Depends(database.get_db)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    temp_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(temp_blog)
    db.commit()
    db.refresh(temp_blog)
    return temp_blog

@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete(id: int, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")
    
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(database.get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    temp_blog = db.query(models.Blog).filter(models.Blog.id == id).update({"title": request.title, "body":request.body})
    db.commit()
    if temp_blog:
        return temp_blog
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")