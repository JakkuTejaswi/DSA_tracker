from fastapi import APIRouter, Depends, HTTPException
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
    db: Session = Depends(get_db)
):
    """
    Synchronously send a password-reset link if the email is registered.
    Returns email_found flag so frontend can inform the user accurately.
    """
    email = request.email.strip().lower()
    user = crud.get_user_by_email(db, email)

    if not user:
        return {
            "message": "No account found with this email address.",
            "email_found": False
        }

    reset_token = crud.create_reset_token(db, user.id)

    # Send synchronously so we can detect and report real failures
    sent, error = send_password_reset_email(
        to_email=user.email,
        reset_token=reset_token
    )

    if not sent:
        print(f"[forgot-password] Email delivery failed for {email}: {error}")
        raise HTTPException(
            status_code=503,
            detail="We could not send the reset email right now. Please try again in a few minutes."
        )

    return {
        "message": "A password reset link has been sent to your email.",
        "email_found": True
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