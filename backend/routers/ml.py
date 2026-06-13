from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from dependencies import get_db
from dependencies_auth import get_current_user_id

import crud
import joblib

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)

model = joblib.load(
    "model.pkl"
)

@router.get("/readiness")
def readiness_score(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(
        get_current_user_id
    )
):

    features = crud.readiness_features(
        db,
        current_user_id
    )

    prediction = model.predict(
        [[
            features["easy"],
            features["medium"],
            features["hard"],
            features["streak"]
        ]]
    )[0]

    return {
        "interview_readiness_score":
            round(prediction, 2),

        "stats": features
    }