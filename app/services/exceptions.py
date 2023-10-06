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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class NotMemberException(HTTPException):
    def __init__(self, detail="User is not a member of the company"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class NotAdminException(HTTPException):
    def __init__(self, detail="User not a admin of company"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotValidQuizException(HTTPException):
    def __init__(self, detail="Quiz must have at least 2 questions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )