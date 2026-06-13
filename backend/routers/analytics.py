from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from schemas import SolveProblemRequest
from dependencies_auth import get_current_user_id
import crud

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.post("/solve")
def solve_problem(
    request: SolveProblemRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        get_current_user_id
    )
):

    solved = crud.mark_problem_solved(
    db,
    current_user_id,
    request.problem_id
)

    return {
        "message": "Problem Solved",
        "record_id": solved.id
    }

@router.get("/")
def get_analytics(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        get_current_user_id
    )
):
    total = crud.total_solved(
    db,
    current_user_id
)
    print("TOTAL:", total)

    topics = crud.topic_analytics(
    db,
    current_user_id
)
    print("TOPICS:", topics)

    difficulty = crud.difficulty_analytics(
    db,
    current_user_id
)
    print("DIFFICULTY:", difficulty)

    return {
        "total_solved": total,
        "topic_breakdown": topics,
        "difficulty_breakdown": difficulty
    }

@router.get("/streak/{user_id}")
def streak(user_id: int, db: Session = Depends(get_db)):

    return {
        "current_streak":
            crud.current_streak(
                db,
                user_id
            ),

        "longest_streak":
            crud.longest_streak(
                db,
                user_id
            )
    }

@router.get("/recommend/{user_id}")
def recommend(
    user_id: int,
    db: Session = Depends(get_db)
):

    return crud.recommend_problems(
        db,
        user_id
    )

@router.get("/dashboard/{user_id}")
def get_user_dashboard(
    user_id: int,
    db: Session = Depends(get_db)
):

    return crud.dashboard_stats(
        db,
        user_id
    )

@router.get("/dashboard")
def dashboard_current(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        get_current_user_id
    )
):

    total = crud.total_solved_count(
        db,
        current_user_id
    )

    difficulty = crud.difficulty_breakdown(
        db,
        current_user_id
    )

    streak = crud.calculate_streak(
        db,
        current_user_id
    )

    return {
        "total_solved": total,
        "easy": difficulty.get("Easy", 0) or difficulty.get("easy", 0),
        "medium": difficulty.get("Medium", 0) or difficulty.get("medium", 0),
        "hard": difficulty.get("Hard", 0) or difficulty.get("hard", 0),
        "current_streak": streak
    }