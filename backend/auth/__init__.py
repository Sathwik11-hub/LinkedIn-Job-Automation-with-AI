"""
Authentication module for AutoAgentHire system.
"""

from .auth_service import (
    AuthService,
    CredentialVault,
    get_auth_service,
    get_credential_vault
)

__all__ = [
    'AuthService',
    'CredentialVault',
    'get_auth_service',
    'get_credential_vault'
]
