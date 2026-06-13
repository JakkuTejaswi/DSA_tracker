from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from dependencies import get_db

import crud

from schemas import (
    ProblemCreate,
    ProblemResponse,
    UserProblemResponse
)
from dependencies_auth import get_current_user_id

router = APIRouter(
    prefix="/problems",
    tags=["Problems"]
)
@router.post(
    "/",
    response_model=ProblemResponse
)
def create_problem(
    problem: ProblemCreate,
    db: Session = Depends(get_db)
):

    return crud.create_problem(
        db,
        problem
    )

@router.get(
    "/",
    response_model=list[ProblemResponse]
)
def get_all_problems(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    """Fetch all problems with optional server-side search."""
    return crud.get_problems(db, skip=skip, limit=limit, search=search)

@router.get(
    "/{problem_id}",
    response_model=ProblemResponse
)
def get_problem(
    problem_id: int,
    db: Session = Depends(get_db)
):

    problem = crud.get_problem(
        db,
        problem_id
    )

    if not problem:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return problem

@router.put(
    "/{problem_id}",
    response_model=ProblemResponse
)
def update_problem(
    problem_id: int,
    problem: ProblemCreate,
    db: Session = Depends(get_db)
):

    updated = crud.update_problem(
        db,
        problem_id,
        problem
    )

    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return updated

@router.delete("/{problem_id}")
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db)
):

    deleted = crud.delete_problem(
        db,
        problem_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return {
        "message": "Problem deleted"
    }
    
@router.get("/topic/{topic}")
def filter_topic(
    topic: str,
    db: Session = Depends(get_db)
):

    return crud.get_problems_by_topic(
        db,
        topic
    )
    
@router.get(
    "/difficulty/{difficulty}"
)
def filter_difficulty(
    difficulty: str,
    db: Session = Depends(get_db)
):

    return crud.get_problems_by_difficulty(
        db,
        difficulty
    )

@router.post("/solve/{problem_id}", response_model=UserProblemResponse)
def solve_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Mark a problem as solved for the current user."""
    return crud.mark_problem_solved(db, current_user_id, problem_id)

@router.get("/recommendations", response_model=list[ProblemResponse])
def get_recommendations(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Get personalized problem recommendations based on solved topics."""
    return crud.recommend_problems(db, current_user_id)