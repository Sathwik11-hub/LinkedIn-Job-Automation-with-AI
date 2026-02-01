"""
Authentication routes for user management.

Endpoints:
- POST /auth/register - Register new user
- POST /auth/login - Login and get JWT token
- POST /auth/logout - Logout (client-side token removal)
- GET /auth/me - Get current user info
- POST /auth/credentials/linkedin - Store LinkedIn credentials
- GET /auth/credentials/linkedin - Get LinkedIn credentials (decrypted)
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from backend.auth import get_auth_service, get_credential_vault, AuthService, CredentialVault
from backend.auth.middleware import require_auth, get_current_user
from backend.database.connection import get_db
from backend.database import models, crud


router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    phone: Optional[str]
    created_at: str


class LinkedInCredentials(BaseModel):
    email: str
    password: str


class LinkedInCredentialsResponse(BaseModel):
    email: str
    stored: bool


# Routes

@router.post("/register", response_model=TokenResponse)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user.
    
    Returns JWT token for immediate login.
    """
    # Check if user exists
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = auth_service.hash_password(user_data.password)
    
    # Create user
    user = models.User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create token
    token = auth_service.create_session_token(user.id, user.email)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login with email and password.
    
    Returns JWT token.
    """
    # Get user
    user = crud.get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not auth_service.verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create token
    token = auth_service.create_session_token(user.id, user.email)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user's information.
    """
    user = crud.get_user(db, current_user["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


@router.post("/credentials/linkedin", response_model=LinkedInCredentialsResponse)
async def store_linkedin_credentials(
    credentials: LinkedInCredentials,
    current_user: dict = Depends(require_auth),
    db: Session = Depends(get_db),
    vault: CredentialVault = Depends(get_credential_vault)
):
    """
    Store LinkedIn credentials securely (encrypted).
    """
    user_id = current_user["user_id"]
    
    # Encrypt credentials
    encrypted_data = vault.store_linkedin_credentials(
        user_id=user_id,
        email=credentials.email,
        password=credentials.password
    )
    
    # Store in database
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if credentials already exist
    existing_cred = db.query(models.Credential).filter(
        models.Credential.user_id == user_id,
        models.Credential.service == "linkedin"
    ).first()
    
    if existing_cred:
        # Update existing
        existing_cred.username = credentials.email
        existing_cred.encrypted_value = encrypted_data["encrypted_password"]
    else:
        # Create new
        cred = models.Credential(
            user_id=user_id,
            service="linkedin",
            username=credentials.email,
            encrypted_value=encrypted_data["encrypted_password"]
        )
        db.add(cred)
    
    db.commit()
    
    return {
        "email": credentials.email,
        "stored": True
    }


@router.get("/credentials/linkedin")
async def get_linkedin_credentials(
    current_user: dict = Depends(require_auth),
    db: Session = Depends(get_db),
    vault: CredentialVault = Depends(get_credential_vault)
):
    """
    Get LinkedIn credentials (decrypted).
    
    SECURITY: Only returns credentials for the authenticated user.
    """
    user_id = current_user["user_id"]
    
    # Get credentials from database
    cred = db.query(models.Credential).filter(
        models.Credential.user_id == user_id,
        models.Credential.service == "linkedin"
    ).first()
    
    if not cred:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LinkedIn credentials not found"
        )
    
    # Decrypt credentials
    decrypted = vault.retrieve_linkedin_credentials({
        "user_id": user_id,
        "email": cred.username,
        "encrypted_password": cred.encrypted_value
    })
    
    return {
        "email": decrypted["email"],
        "password": decrypted["password"]
    }


@router.post("/logout")
async def logout():
    """
    Logout endpoint (for documentation).
    
    Actual logout is handled client-side by removing the JWT token.
    Server-side token invalidation would require a token blacklist.
    """
    return {"message": "Logout successful. Please remove your token on the client side."}
