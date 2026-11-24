import pytest
from app.services.auth_services import AuthService


def test_register_user_hashes_password(app):
    user = AuthService.register_user("test@example.com", "password123", "Test User")

    assert user.id is not None
    assert user.password_hash != "password123"      # no está en plano
    assert user.check_password("password123") is True
    assert user.check_password("wrong") is False


def test_register_duplicate_email_raises(app):
    AuthService.register_user("dup@example.com", "password123", "A")
    with pytest.raises(ValueError, match="ya está registrado"):
        AuthService.register_user("dup@example.com", "otra12345", "B")


def test_authenticate_wrong_password_raises(app):
    AuthService.register_user("u@example.com", "password123", "U")
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        AuthService.authenticate("u@example.com", "incorrecta")


def test_authenticate_nonexistent_user_raises(app):
    with pytest.raises(ValueError, match="Credenciales inválidas"):
        AuthService.authenticate("noexiste@example.com", "password123")