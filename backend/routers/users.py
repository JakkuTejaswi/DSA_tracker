from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from dependencies import get_db
import crud
from schemas import (
    UserCreate,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from auth import verify_password, create_access_token
from email_utils import send_password_reset_email

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    return crud.create_user(db, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Send a password-reset link to the user's email.
    Always returns 200 to avoid leaking whether an email is registered.
    """
    user = crud.get_user_by_email(db, request.email)
    if user:
        reset_token = crud.create_reset_token(db, user.id)
        success = send_password_reset_email(request.email, reset_token)
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to send reset email. Please check server logs."
            )

    return {
        "message": "If that email is registered, a reset link has been sent."
    }


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    success = crud.reset_user_password(db, request.token, request.new_password)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )
    return {"message": "Password reset successfully. Please login with your new password."}