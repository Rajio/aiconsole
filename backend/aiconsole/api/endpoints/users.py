from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

from aiconsole.core.database.manager import DatabaseManager
from aiconsole.core.users.service import UserService
from aiconsole.core.users.types import UserProfile

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: str
    updated_at: str


def get_user_service() -> UserService:
    db = DatabaseManager()
    return UserService(db)


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    # Перевірка чи користувач вже існує
    if user_service.get_user_by_email(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user_service.get_user_by_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Створення нового користувача
    password_hash = pwd_context.hash(user.password)
    new_user = user_service.create_user(username=user.username, email=user.email, password_hash=password_hash)
    return new_user


@router.get("/users/me", response_model=UserResponse)
def get_current_user(token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)):
    # TODO: Реалізувати отримання користувача з токена
    user = user_service.get_user_by_id(token)  # Тимчасово використовуємо token як user_id
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user


@router.put("/users/me", response_model=UserResponse)
def update_current_user(
    profile: UserProfile, token: str = Depends(oauth2_scheme), user_service: UserService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(token)  # Тимчасово використовуємо token як user_id
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    updated_user = user_service.update_user_profile(token, profile)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_username(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # TODO: Реалізувати генерацію JWT токена
    return {"access_token": user.id, "token_type": "bearer"}  # Тимчасово повертаємо user_id як токен
