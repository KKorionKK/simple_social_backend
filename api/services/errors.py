from fastapi import status, HTTPException


class CustomErrors:
    CouldNotValidateCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    IncorrectCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    AlreadySubscribed = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You have already subscribed to a user",
    )
    EmailInUse = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You have already subscribed to a user",
    )
    UserNotFound = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Requested user not found",
    )
    AlreadyLiked = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You have already liked this",
    )
    GoneComment = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="There is no that comment anymore",
    )
    EntityNotFound = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="The requested object not found"
    )
