from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from .. import schemas, database, models, hashing, token

from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["authentication"]

)

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username not found")
    else:
        if hashing.verify_password(request.password, user.password):
            access_token = token.create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        