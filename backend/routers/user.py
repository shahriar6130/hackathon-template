from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import schemas, models, database  # Clean absolute import
from routers.authentication import get_current_user  # Clean absolute import
import bcrypt

router = APIRouter(
    tags=['users']
)

# Signup Port
@router.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Clean native bcrypt implementation (Bypasses passlib error completely)
    password_bytes = user.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Show user profile port
@router.get("/profile", response_model=schemas.UserResponse)
def show_profile(current_user: models.User = Depends(get_current_user)):
    return current_user