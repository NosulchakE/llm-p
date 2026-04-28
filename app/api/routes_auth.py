# app/api/routes_auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Регистрация нового пользователя"""
    try:
        user = await auth_usecase.register(request.email, request.password)
        return user
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Логин, получение JWT токена"""
    try:
        token = await auth_usecase.login(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Получение профиля текущего пользователя"""
    try:
        user = await auth_usecase.get_profile(user_id)
        return user
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
