"""
Authentication Service for AutoAgentHire System

Provides:
- User authentication with JWT tokens
- Password hashing and verification
- Credential encryption for LinkedIn accounts
- Session management
- Multi-user support
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.fernet import Fernet
import base64
from pathlib import Path


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# Credential encryption key
ENCRYPTION_KEY_FILE = Path("data/.encryption_key")


class AuthService:
    """
    Handles authentication, password hashing, and credential encryption.
    """
    
    def __init__(self):
        self.pwd_context = pwd_context
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
    
    def _get_or_create_encryption_key(self) -> bytes:
        """
        Get or create encryption key for sensitive data.
        Key is stored in data/.encryption_key and should be backed up securely.
        """
        if ENCRYPTION_KEY_FILE.exists():
            with open(ENCRYPTION_KEY_FILE, 'rb') as f:
                return f.read()
        
        # Create new key
        key = Fernet.generate_key()
        ENCRYPTION_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(ENCRYPTION_KEY_FILE, 'wb') as f:
            f.write(key)
        
        # Set restrictive permissions
        os.chmod(ENCRYPTION_KEY_FILE, 0o600)
        
        return key
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password for storing.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Stored hash to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_credential(self, credential: str) -> str:
        """
        Encrypt a credential (password, API key, etc.).
        
        Args:
            credential: Plain text credential
            
        Returns:
            Encrypted credential (base64 encoded)
        """
        encrypted = self.cipher.encrypt(credential.encode())
        return base64.b64encode(encrypted).decode()
    
    def decrypt_credential(self, encrypted_credential: str) -> str:
        """
        Decrypt a credential.
        
        Args:
            encrypted_credential: Encrypted credential (base64 encoded)
            
        Returns:
            Decrypted credential
        """
        try:
            encrypted_bytes = base64.b64decode(encrypted_credential.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt credential: {str(e)}")
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in token (typically user_id, email)
            expires_delta: Token expiration time (default: 30 days)
            
        Returns:
            JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token data if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    def create_session_token(self, user_id: int, email: str) -> str:
        """
        Create a session token for a user.
        
        Args:
            user_id: User ID
            email: User email
            
        Returns:
            Session token
        """
        return self.create_access_token({
            "user_id": user_id,
            "email": email,
            "type": "session"
        })
    
    def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a session token.
        
        Args:
            token: Session token
            
        Returns:
            User data if valid, None otherwise
        """
        payload = self.verify_token(token)
        
        if payload and payload.get("type") == "session":
            return {
                "user_id": payload.get("user_id"),
                "email": payload.get("email")
            }
        
        return None


class CredentialVault:
    """
    Secure storage for LinkedIn and other credentials.
    Uses encryption for all sensitive data.
    """
    
    def __init__(self, auth_service: Optional[AuthService] = None):
        self.auth_service = auth_service or AuthService()
    
    def store_linkedin_credentials(
        self,
        user_id: int,
        email: str,
        password: str
    ) -> Dict[str, str]:
        """
        Store LinkedIn credentials securely.
        
        Args:
            user_id: User ID
            email: LinkedIn email
            password: LinkedIn password
            
        Returns:
            Dictionary with encrypted credentials
        """
        return {
            "user_id": user_id,
            "email": email,  # Email is not sensitive, store as-is
            "encrypted_password": self.auth_service.encrypt_credential(password)
        }
    
    def retrieve_linkedin_credentials(
        self,
        encrypted_data: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Retrieve and decrypt LinkedIn credentials.
        
        Args:
            encrypted_data: Dictionary with encrypted credentials
            
        Returns:
            Dictionary with decrypted credentials
        """
        return {
            "user_id": encrypted_data.get("user_id"),
            "email": encrypted_data.get("email"),
            "password": self.auth_service.decrypt_credential(
                encrypted_data.get("encrypted_password", "")
            )
        }
    
    def store_api_key(
        self,
        user_id: int,
        service: str,
        api_key: str
    ) -> Dict[str, str]:
        """
        Store API key securely.
        
        Args:
            user_id: User ID
            service: Service name (e.g., 'gemini', 'openai', 'github')
            api_key: API key to encrypt
            
        Returns:
            Dictionary with encrypted API key
        """
        return {
            "user_id": user_id,
            "service": service,
            "encrypted_api_key": self.auth_service.encrypt_credential(api_key)
        }
    
    def retrieve_api_key(
        self,
        encrypted_data: Dict[str, str]
    ) -> str:
        """
        Retrieve and decrypt API key.
        
        Args:
            encrypted_data: Dictionary with encrypted API key
            
        Returns:
            Decrypted API key
        """
        return self.auth_service.decrypt_credential(
            encrypted_data.get("encrypted_api_key", "")
        )


# Global instances
_auth_service = AuthService()
_credential_vault = CredentialVault(_auth_service)


def get_auth_service() -> AuthService:
    """Get global authentication service instance."""
    return _auth_service


def get_credential_vault() -> CredentialVault:
    """Get global credential vault instance."""
    return _credential_vault
