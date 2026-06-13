from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from datetime import datetime
from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True)

    email = Column(String(100), unique=True)

    password = Column(String(255))


class Problem(Base):

    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))

    difficulty = Column(String(50))

    topic = Column(String(100))

    leetcode_link = Column(String(500))


class UserProblem(Base):

    __tablename__ = "user_problems"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    problem_id = Column(
        Integer,
        ForeignKey("problems.id")
    )

    status = Column(
        String(50),
        default="Solved"
    )

    solved_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class PasswordResetToken(Base):

    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    token = Column(String(255), unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    used = Column(Integer, default=0)