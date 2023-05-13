from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, models, database

from ..hashing import get_password_hash, verify_password

router = APIRouter(
    tags=["User"],
    prefix="/user"
)

@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    newUser = models.User(name=request.name, email=request.email, password=get_password_hash(request.password))
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.post("/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_202_ACCEPTED)
def get_user(id: int, db: Session = Depends(database.get_db)):
    newUser = db.query(models.User).filter(models.User.id == id).first()
    if newUser:
        return newUser
    else:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return f"Blog with id: {id} not found"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id: {id} not found")

@router.get("/del")
def delete_user(db: Session = Depends(database.get_db)):
    db.query(models.User).delete()
    db.commit()
    return "OK"