from fastapi import HTTPException, status


class CredentialException(HTTPException):
    def __init__(self, detail="Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ActionPermissionException(HTTPException):
    def __init__(self, detail="You dont have permission to do this"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class AlreadyMemberException(HTTPException):
    def __init__(self, detail="User already member in this company"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotMemberException(HTTPException):
    def __init__(self, detail="User not member in this company"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )