from modelos import Usuario

def criar_usuarios_padrao(db):
    # Admin padrão
    if not Usuario.query.filter_by(email="admin@helpdesk.com").first():
        u = Usuario(email="admin@helpdesk.com", role="admin")
        u.definir_senha("123456")
        db.session.add(u)

    # User padrão
    if not Usuario.query.filter_by(email="user@helpdesk.com").first():
        u = Usuario(email="user@helpdesk.com", role="user")
        u.definir_senha("123456")
        db.session.add(u)

    db.session.commit()
