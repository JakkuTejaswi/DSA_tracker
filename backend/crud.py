from sqlalchemy.orm import Session
from models import User, PasswordResetToken
from schemas import UserCreate
from auth import hash_password
from models import Problem
from schemas import ProblemCreate
from sqlalchemy import func
from datetime import date, timedelta, datetime
from datetime import date, timedelta, datetime, timezone
from recommendations import TOPIC_FLOW
import secrets


def create_reset_token(db: Session, user_id: int):
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user_id).delete()
    import secrets
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    db_token = PasswordResetToken(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    return token


def get_valid_reset_token(db: Session, token: str):
    """Return the reset token record if it is valid (exists, not used, not expired)."""
    record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.used == 0
    ).first()

    if not record:
        return None
    if record.expires_at < datetime.utcnow():
        return None
    return record


def reset_user_password(db: Session, token: str, new_password: str) -> bool:
    """Validate token and update the user's password. Returns True on success."""
    record = get_valid_reset_token(db, token)
    if not record:
        return False

    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        return False

    user.password = hash_password(new_password)
    record.used = 1
    db.commit()
    return True


def create_user(
    db: Session,
    user: UserCreate
):

    hashed = hash_password(
        user.password
    )

    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()

def get_user_by_username(
    db: Session,
    username: str
):

    return db.query(User).filter(
        User.username == username
    ).first()

def create_problem(
    db: Session,
    problem: ProblemCreate
):

    db_problem = Problem(
        title=problem.title,
        difficulty=problem.difficulty,
        topic=problem.topic,
        leetcode_link=problem.leetcode_link
    )

    db.add(db_problem)

    db.commit()

    db.refresh(db_problem)

    return db_problem


def get_problems(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(Problem)
    if search:
        query = query.filter(Problem.title.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


def get_problem(
    db: Session,
    problem_id: int
):

    return db.query(Problem).filter(
        Problem.id == problem_id
    ).first()


def update_problem(
    db: Session,
    problem_id: int,
    problem_data: ProblemCreate
):

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        return None

    problem.title = problem_data.title
    problem.difficulty = problem_data.difficulty
    problem.topic = problem_data.topic
    problem.leetcode_link = problem_data.leetcode_link

    db.commit()

    db.refresh(problem)

    return problem


def delete_problem(
    db: Session,
    problem_id: int
):

    problem = db.query(Problem).filter(
        Problem.id == problem_id
    ).first()

    if not problem:
        return None

    db.delete(problem)

    db.commit()

    return problem

def get_problems_by_topic(
    db: Session,
    topic: str
):

    return db.query(Problem).filter(
        Problem.topic == topic
    ).all()

def get_problems_by_difficulty(
    db: Session,
    difficulty: str
):

    return db.query(Problem).filter(
        Problem.difficulty == difficulty
    ).all()

from models import UserProblem


def mark_problem_solved(
    db: Session,
    user_id: int,
    problem_id: int
):

    existing = db.query(
        UserProblem
    ).filter(
        UserProblem.user_id == user_id,
        UserProblem.problem_id == problem_id
    ).first()

    if existing:
        return existing

    solved = UserProblem(
        user_id=user_id,
        problem_id=problem_id,
        status="Solved"
    )

    db.add(solved)

    db.commit()

    db.refresh(solved)

    return solved


def total_solved(
    db: Session,
    user_id: int
):

    return db.query(
        UserProblem
    ).filter(
        UserProblem.user_id == user_id
    ).count()


def topic_analytics(
    db: Session,
    user_id: int
):

    result = (
        db.query(
            Problem.topic,
            func.count(UserProblem.id)
        )
        .join(
            UserProblem,
            Problem.id == UserProblem.problem_id
        )
        .filter(
            UserProblem.user_id == user_id
        )
        .group_by(
            Problem.topic
        )
        .all()
    )

    return [
        {
            "topic": topic,
            "count": count
        }
        for topic, count in result
    ]

def difficulty_analytics(
    db: Session,
    user_id: int
):

    result = (
        db.query(
            Problem.difficulty,
            func.count(UserProblem.id)
        )
        .join(
            UserProblem,
            Problem.id == UserProblem.problem_id
        )
        .filter(
            UserProblem.user_id == user_id
        )
        .group_by(
            Problem.difficulty
        )
        .all()
    )

    return [
        {
            "difficulty": difficulty,
            "count": count
        }
        for difficulty, count in result
    ]

def current_streak(db, user_id):

    dates = (
        db.query(UserProblem.solved_at)
        .filter(UserProblem.user_id == user_id)
        .all()
    )

    solved_dates = {
        row[0].date()
        for row in dates
        if row[0]
    }

    streak = 0
    today = date.today()

    while today in solved_dates:
        streak += 1
        today -= timedelta(days=1)

    return streak

def longest_streak(db, user_id):

    dates = (
        db.query(UserProblem.solved_at)
        .filter(UserProblem.user_id == user_id)
        .all()
    )

    solved_dates = sorted(
        {
            row[0].date()
            for row in dates
            if row[0]
        }
    )

    if not solved_dates:
        return 0

    longest = 1
    current = 1

    for i in range(1, len(solved_dates)):

        if solved_dates[i] == solved_dates[i-1] + timedelta(days=1):
            current += 1
            longest = max(longest, current)

        else:
            current = 1

    return longest

def dashboard_stats(
    db: Session,
    user_id: int
):

    total = total_solved(
        db,
        user_id
    )

    difficulty_data = difficulty_analytics(
        db,
        user_id
    )

    stats = {
        "easy": 0,
        "medium": 0,
        "hard": 0
    }

    for item in difficulty_data:

        stats[
            item["difficulty"].lower()
        ] = item["count"]

    return {
    "total_solved": total,
    "current_streak":
        current_streak(
            db,
            user_id
        ),
    "longest_streak":
        longest_streak(
            db,
            user_id
        ),
    "easy": stats["easy"],
    "medium": stats["medium"],
    "hard": stats["hard"]
}


def recommend_problems(
    db: Session,
    user_id: int
):

    solved_topics = (

        db.query(
            Problem.topic
        )

        .join(
            UserProblem,
            Problem.id ==
            UserProblem.problem_id
        )

        .filter(
            UserProblem.user_id ==
            user_id
        )

        .distinct()

        .all()
    )

    solved_topics = [
        topic[0]
        for topic in solved_topics
    ]

    next_topics = []

    for topic in solved_topics:

        if topic in TOPIC_FLOW:

            next_topics.extend(
                TOPIC_FLOW[topic]
            )

    recommendations = (

        db.query(Problem)

        .filter(
            Problem.topic.in_(
                next_topics
            )
        )

        .all()
    )

    return  [

    {
        "id": p.id,
        "title": p.title,
        "topic": p.topic,
        "difficulty": p.difficulty,
        "leetcode_link":
            p.leetcode_link
    }

    for p in recommendations
]
    
def readiness_features(
    db: Session,
    user_id: int
):

    difficulty_data = difficulty_analytics(
        db,
        user_id
    )

    stats = {
        "easy": 0,
        "medium": 0,
        "hard": 0
    }

    for item in difficulty_data:

        stats[
            item["difficulty"].lower()
        ] = item["count"]

    return {
        "easy": stats["easy"],
        "medium": stats["medium"],
        "hard": stats["hard"],
        "streak": current_streak(
            db,
            user_id
        )
    }

def difficulty_breakdown(
    db: Session,
    user_id: int
):

    result = (
        db.query(
            Problem.difficulty,
            func.count(UserProblem.id)
        )
        .join(
            UserProblem,
            Problem.id == UserProblem.problem_id
        )
        .filter(
            UserProblem.user_id == user_id
        )
        .group_by(
            Problem.difficulty
        )
        .all()
    )

    return {
        difficulty: count
        for difficulty, count in result
    }

def total_solved_count(
    db: Session,
    user_id: int
):

    return (
        db.query(UserProblem)
        .filter(
            UserProblem.user_id == user_id
        )
        .count()
    )

from datetime import date, timedelta

def calculate_streak(
    db: Session,
    user_id: int
):

    solved_dates = (
        db.query(UserProblem.solved_at)
        .filter(
            UserProblem.user_id == user_id
        )
        .order_by(
            UserProblem.solved_at.desc()
        )
        .all()
    )

    solved_dates = [
        d[0].date()
        for d in solved_dates
    ]

    streak = 0
    current_day = date.today()

    while current_day in solved_dates:

        streak += 1

        current_day -= timedelta(days=1)

    return streak