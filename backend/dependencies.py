# backend/dependencies.py

from fastapi import Depends, HTTPException, status
from typing import List
import schemas
from auth_utils import get_current_user

def role_checker(allowed_roles: List[str]):
    def check_roles(current_user: schemas.User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )
        return current_user
    return check_roles