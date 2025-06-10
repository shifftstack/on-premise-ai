from fastapi import APIRouter, Depends, HTTPException, status
from app.services import user_management, audit
from app.models.user import UserResponse
from app.core.security import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/admin", tags=["admin"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload or not payload.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return payload

@router.get("/users", response_model=list[UserResponse])
def list_users(admin=Depends(get_current_admin)):
    audit.log_action("list_users", admin["sub"])
    return user_management.list_users()

@router.delete("/users/{email}")
def delete_user(email: str, admin=Depends(get_current_admin)):
    user_management.delete_user(email)
    audit.log_action("delete_user", admin["sub"], target=email)
    return {"detail": "User deleted"} 