# Projeto 3 — Sistema de Chamados (HelpDesk)


Sistema completo com Backend (API REST) + Front (React simples).

## Regras
- Usuário (role: user) cria chamados
- Admin (role: admin) responde e fecha chamados

## Rodar backend
```bash
cd "Projeto 3 - Sistema de Chamados (HelpDesk API + React)/backend"
python -m venv .venv
pip install -r requirements.txt
flask --app app run --debug
```

## Rodar front
Em outro terminal:
```bash
cd "Projeto 3 - Sistema de Chamados (HelpDesk API + React)/frontend"
npm install
npm run dev
```

## Usuários padrão
Ao iniciar o backend pela 1ª vez ele cria automaticamente:
- admin: `admin@helpdesk.com` / `123456`
- user: `user@helpdesk.com` / `123456`

