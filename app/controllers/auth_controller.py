from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..services.auth_services import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json() or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")
    full_name = data.get("full_name", "").strip()

    # Validación básica (en el Día 5 la movemos a schemas/)
    if not email or not password or not full_name:
        return jsonify({"error": "email, password y full_name son obligatorios"}), 400
    if len(password) < 8:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), 400
    if "@" not in email:
        return jsonify({"error": "Email inválido"}), 400

    try:
        user = AuthService.register_user(email, password, full_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({"message": "Usuario creado", "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "email y password son obligatorios"}), 400

    try:
        user = AuthService.authenticate(email, password)
    except ValueError as e:
        return jsonify({"error": str(e)}), 401

    # Claims: datos que viajan dentro del token
    additional_claims = {"role": user.role, "email": user.email}
    token = create_access_token(
        identity=str(user.id),
        additional_claims=additional_claims,
    )

    return jsonify({"access_token": token, "user": user.to_dict()}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    from ..models.user import User
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict()), 200