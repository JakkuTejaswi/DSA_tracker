from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from auth import SECRET_KEY
from auth import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

def get_current_user_id(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )