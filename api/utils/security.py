"""Utilidades de seguridad."""
import hashlib


def hash_password(password: str) -> str:
    """Hash de contraseña usando SHA-256 (para futura autenticación)."""
    return hashlib.sha256(password.encode()).hexdigest()