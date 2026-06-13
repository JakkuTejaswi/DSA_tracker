from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserProblemResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    status: str
    solved_at: Optional[datetime]

    class Config:
        from_attributes = True

class ReadinessRequest(BaseModel):

    easy: int
    medium: int
    hard: int
    streak: int

class UserCreate(BaseModel):

    username: str

    email: str

    password: str


class UserResponse(BaseModel):

    id: int

    username: str

    email: str

    class Config:

        from_attributes = True


class ProblemCreate(BaseModel):

    title: str

    difficulty: str

    topic: str

    leetcode_link: str


class ProblemResponse(ProblemCreate):

    id: int

    class Config:

        from_attributes = True

class LoginRequest(BaseModel):

    email: str

    password: str

class SolveProblemRequest(BaseModel):

    problem_id: int


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str