import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///helpdesk.sqlite3")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)

    from rotas.auth import bp_auth
    from rotas.chamados import bp_chamados
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_chamados)

    @app.get("/")
    def raiz():
        return jsonify({"status":"ok","projeto":"HelpDesk"})

    with app.app_context():
        from modelos import Usuario, Chamado, Resposta  # noqa
        db.create_all()
        from seed import criar_usuarios_padrao
        criar_usuarios_padrao(db)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
