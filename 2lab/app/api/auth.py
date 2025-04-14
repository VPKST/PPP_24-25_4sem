from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.db.session import async_session
from app.cruds.user import get_user_by_email, create_user, pwd_context
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.config import settings

router = APIRouter()

def create_token(user_id: int):
    token = jwt.encode({"user_id": user_id}, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/sign-up/", response_model=UserResponse)
async def sign_up(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    new_user = await create_user(db, user.email, user.password)
    token = create_token(new_user.id)
    return UserResponse(id=new_user.id, email=new_user.email, token=token)

@router.post("/login/", response_model=UserResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_email(db, user.email)
    if not existing_user or not pwd_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    token = create_token(existing_user.id)
    return UserResponse(id=existing_user.id, email=existing_user.email, token=token)
