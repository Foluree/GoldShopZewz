from fastapi import HTTPException, status

def UntorizatedError(detail):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail
    )

UserAllNoneExit = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User allredy there is."
)

NoneCorrectEmailOrPassword = UntorizatedError(detail="NoneCorrectEmailOrPassword")