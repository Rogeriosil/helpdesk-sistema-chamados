from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from modelos import Usuario

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")

@bp_auth.post("/login")
def login():
    dados = request.get_json(silent=True) or {}
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro":"Credenciais inválidas."}), 401

    token = create_access_token(identity=str(usuario.id), additional_claims={"role": usuario.role, "email": usuario.email})
    return jsonify({"access_token": token, "usuario": usuario.para_dict()})
