from ..models.user import User
from ..extensions import db


class AuthService:

    @staticmethod
    def register_user(email: str, password: str, full_name: str) -> User:
        # Regla de negocio: email único
        if User.query.filter_by(email=email.lower()).first():
            raise ValueError("El email ya está registrado")

        user = User(
            email=email.lower(),
            full_name=full_name,
            role="customer",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email: str, password: str) -> User:
        user = User.query.filter_by(email=email.lower()).first()

        # Mensaje genérico: no revelar si el email existe o no
        if not user or not user.check_password(password):
            raise ValueError("Credenciales inválidas")

        if not user.is_active:
            raise ValueError("Usuario inactivo")

        return user