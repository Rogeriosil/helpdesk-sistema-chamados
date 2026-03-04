from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db
from modelos import Chamado, Resposta, Usuario

bp_chamados = Blueprint("chamados", __name__, url_prefix="/chamados")

def _role():
    return (get_jwt() or {}).get("role", "user")

@bp_chamados.post("")
@jwt_required()
def criar():
    dados = request.get_json(silent=True) or {}
    titulo = (dados.get("titulo") or "").strip()
    descricao = (dados.get("descricao") or "").strip()
    if not titulo or not descricao:
        return jsonify({"erro":"Informe titulo e descricao."}), 400

    usuario_id = int(get_jwt_identity())
    chamado = Chamado(titulo=titulo, descricao=descricao, usuario_id=usuario_id)
    db.session.add(chamado)
    db.session.commit()
    return jsonify(chamado.para_dict()), 201

@bp_chamados.get("")
@jwt_required()
def listar():
    role = _role()
    usuario_id = int(get_jwt_identity())
    if role == "admin":
        chamados = Chamado.query.order_by(Chamado.id.desc()).all()
    else:
        chamados = Chamado.query.filter_by(usuario_id=usuario_id).order_by(Chamado.id.desc()).all()
    return jsonify([c.para_dict() for c in chamados])

@bp_chamados.get("/<int:chamado_id>")
@jwt_required()
def obter(chamado_id: int):
    role = _role()
    usuario_id = int(get_jwt_identity())
    chamado = Chamado.query.get_or_404(chamado_id)
    if role != "admin" and chamado.usuario_id != usuario_id:
        return jsonify({"erro":"Sem permissão."}), 403
    d = chamado.para_dict()
    d["respostas"] = [r.para_dict() for r in chamado.respostas]
    return jsonify(d)

@bp_chamados.post("/<int:chamado_id>/responder")
@jwt_required()
def responder(chamado_id: int):
    role = _role()
    if role != "admin":
        return jsonify({"erro":"Apenas admin pode responder."}), 403

    dados = request.get_json(silent=True) or {}
    mensagem = (dados.get("mensagem") or "").strip()
    if not mensagem:
        return jsonify({"erro":"Informe a mensagem."}), 400

    chamado = Chamado.query.get_or_404(chamado_id)
    admin_id = int(get_jwt_identity())
    resposta = Resposta(mensagem=mensagem, chamado_id=chamado.id, admin_id=admin_id)
    db.session.add(resposta)
    db.session.commit()
    return jsonify(resposta.para_dict()), 201

@bp_chamados.put("/<int:chamado_id>/status")
@jwt_required()
def alterar_status(chamado_id: int):
    role = _role()
    if role != "admin":
        return jsonify({"erro":"Apenas admin pode alterar status."}), 403

    dados = request.get_json(silent=True) or {}
    status = (dados.get("status") or "").strip().lower()
    if status not in ("aberto", "fechado"):
        return jsonify({"erro":"Status deve ser 'aberto' ou 'fechado'."}), 400

    chamado = Chamado.query.get_or_404(chamado_id)
    chamado.status = status
    db.session.commit()
    return jsonify(chamado.para_dict())

@bp_chamados.get("/dashboard/resumo")
@jwt_required()
def dashboard():
    role = _role()
    if role != "admin":
        return jsonify({"erro":"Apenas admin."}), 403

    total = Chamado.query.count()
    abertos = Chamado.query.filter_by(status="aberto").count()
    fechados = Chamado.query.filter_by(status="fechado").count()
    return jsonify({"total": total, "abertos": abertos, "fechados": fechados})
