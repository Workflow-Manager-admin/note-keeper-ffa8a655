from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import models
from .database_models import User
from .db import get_db
from .auth import hash_password, verify_password, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_user_by_username(db: Session, username: str):
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if user and verify_password(password, user.password_hash):
        return user
    return None

# PUBLIC_INTERFACE
@router.post("/register", summary="Register User", response_model=models.Token)
def register(user_in: models.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    - **username**: Unique desired username
    - **password**: User password (plaintext, will be hashed)
    """
    existing = db.query(User).filter_by(username=user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(
        username=user_in.username,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# PUBLIC_INTERFACE
@router.post("/login", summary="User Login", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return access token.

    - **username**: User's username
    - **password**: User's password
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from JWT token."""
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
