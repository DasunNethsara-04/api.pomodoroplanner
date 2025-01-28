from fastapi import HTTPException
from starlette import status


class Exceptions:
    def __init__(self) -> None:
        pass
    
    def http_400_bad_request_exception(self, detail: str = "Invalid Request") -> HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    
    
    def http_401_unauthorized_exception(self, detail: str = "Incorrect username or password")->HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    
    
    def http_403_forbidden_exception(self, detail: str = "Not authorized to perform this action") -> HTTPException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    
    
    def http_404_not_found_exception(self, detail: str = "Resource not found!") -> HTTPException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    
    
    def http_405_method_not_allowed_exception(self, detail: str = "Method not allowed") -> HTTPException:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=detail)
    
    
    def http_500_internal_server_error_exception(self, detail: str = "Internal Server Error") -> HTTPException:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
    
    
    