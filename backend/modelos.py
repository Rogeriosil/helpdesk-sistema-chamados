from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")  # user|admin

    def definir_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def para_dict(self):
        return {"id": self.id, "email": self.email, "role": self.role}

class Chamado(db.Model):
    __tablename__ = "chamados"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="aberto")  # aberto|fechado
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario = db.relationship("Usuario", backref="chamados")

    def para_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "criado_em": self.criado_em.isoformat(),
            "usuario": self.usuario.para_dict(),
        }

class Resposta(db.Model):
    __tablename__ = "respostas"
    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    chamado_id = db.Column(db.Integer, db.ForeignKey("chamados.id"), nullable=False)
    chamado = db.relationship("Chamado", backref="respostas")

    admin_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    admin = db.relationship("Usuario")

    def para_dict(self):
        return {
            "id": self.id,
            "mensagem": self.mensagem,
            "criado_em": self.criado_em.isoformat(),
            "admin": self.admin.para_dict(),
        }
