from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.models.user import User
from app.schemas.user import RegisterSchema, LoginSchema
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.google_auth import verify_google_token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/google")
def google_login(payload: dict, db: Session = Depends(get_db)):

    token = payload.get("token")

    google_user = verify_google_token(token)

    if not google_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token"
        )

    user = db.query(User).filter(
        User.email == google_user["email"]
    ).first()

    if not user:

        user = User(
            username=google_user.get("name", ""),
            first_name=google_user.get("given_name", ""),
            last_name=google_user.get("family_name", ""),
            email=google_user["email"],
            google_id=google_user["google_id"],
            avatar=google_user.get("picture", ""),
            password=""
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "avatar": user.avatar
        }
    }

@router.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token({
        "user_id": existing_user.id,
        "email": existing_user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": existing_user.id,
            "username": existing_user.username,
            "first_name": existing_user.first_name,
            "last_name": existing_user.last_name,
            "email": existing_user.email,
            "avatar": existing_user.avatar
        }
    }