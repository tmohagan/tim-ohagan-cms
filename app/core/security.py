import os
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme_admin_pass")

def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Validates HTTP Basic Auth credentials using constant-time comparison
    to protect administrative routes and sensitive inbox data.
    """
    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), 
        ADMIN_USERNAME.encode("utf8")
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), 
        ADMIN_PASSWORD.encode("utf8")
    )
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
