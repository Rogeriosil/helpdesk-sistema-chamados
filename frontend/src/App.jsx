import React, { useEffect, useMemo, useState } from "react";
import { api, setToken, getUsuario, setUsuario } from "./api.js";

function Botao({ children, ...props }) {
  return <button style={{ padding: "10px 12px", cursor: "pointer" }} {...props}>{children}</button>;
}

function Caixa({ children }) {
  return <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16, marginTop: 12 }}>{children}</div>;
}

export default function App() {
  const [email, setEmail] = useState("admin@helpdesk.com");
  const [senha, setSenha] = useState("123456");
  const [erro, setErro] = useState("");
  const [usuario, setUsr] = useState(getUsuario());
  const [chamados, setChamados] = useState([]);
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [mensagemResposta, setMensagemResposta] = useState("");
  const [chamadoSelecionado, setChamadoSelecionado] = useState(null);
  const isAdmin = useMemo(() => (usuario?.role === "admin"), [usuario]);

  async function carregarChamados() {
    const lista = await api("/chamados");
    setChamados(lista);
  }

  useEffect(() => {
    if (usuario) carregarChamados().catch(e => setErro(e.message));
  }, [usuario]);

  async function login(e) {
    e.preventDefault();
    setErro("");
    try {
      const r = await api("/auth/login", { method: "POST", body: { email, senha } });
      setToken(r.access_token);
      setUsuario(r.usuario);
      setUsr(r.usuario);
    } catch (err) {
      setErro(err.message);
    }
  }

  async function criarChamado() {
    setErro("");
    try {
      await api("/chamados", { method: "POST", body: { titulo, descricao } });
      setTitulo(""); setDescricao("");
      await carregarChamados();
    } catch (err) {
      setErro(err.message);
    }
  }

  async function abrirChamado(id) {
    setErro("");
    try {
      const d = await api(`/chamados/${id}`);
      setChamadoSelecionado(d);
    } catch (err) {
      setErro(err.message);
    }
  }

  async function responder() {
    setErro("");
    try {
      await api(`/chamados/${chamadoSelecionado.id}/responder`, { method: "POST", body: { mensagem: mensagemResposta } });
      setMensagemResposta("");
      await abrirChamado(chamadoSelecionado.id);
      await carregarChamados();
    } catch (err) {
      setErro(err.message);
    }
  }

  async function fecharChamado() {
    setErro("");
    try {
      await api(`/chamados/${chamadoSelecionado.id}/status`, { method: "PUT", body: { status: "fechado" } });
      await abrirChamado(chamadoSelecionado.id);
      await carregarChamados();
    } catch (err) {
      setErro(err.message);
    }
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    setUsr(null);
    setChamados([]);
    setChamadoSelecionado(null);
  }

  return (
    <div style={{ fontFamily: "system-ui, Segoe UI, Arial", maxWidth: 980, margin: "30px auto", padding: "0 12px" }}>
      <h1>HelpDesk</h1>
      <p style={{ color: "#555" }}>Front simples para consumir a API.</p>

      {erro && <div style={{ background: "#ffe8e8", border: "1px solid #f0b2b2", padding: 12, borderRadius: 10 }}>{erro}</div>}

      {!usuario ? (
        <Caixa>
          <h2>Login</h2>
          <form onSubmit={login} style={{ display: "grid", gap: 10 }}>
            <label>Email<br/>
              <input value={email} onChange={e => setEmail(e.target.value)} style={{ width: "100%", padding: 10 }} />
            </label>
            <label>Senha<br/>
              <input type="password" value={senha} onChange={e => setSenha(e.target.value)} style={{ width: "100%", padding: 10 }} />
            </label>
            <Botao type="submit">Entrar</Botao>
          </form>
          <p style={{ marginTop: 10, color: "#666" }}>
            Dica: admin@helpdesk.com / 123456 ou user@helpdesk.com / 123456
          </p>
        </Caixa>
      ) : (
        <>
          <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" }}>
            <div>
              <b>Logado:</b> {usuario.email} ({usuario.role})
            </div>
            <Botao onClick={logout}>Sair</Botao>
          </div>

          {!isAdmin && (
            <Caixa>
              <h2>Novo chamado</h2>
              <label>Título<br/>
                <input value={titulo} onChange={e => setTitulo(e.target.value)} style={{ width: "100%", padding: 10 }} />
              </label>
              <label style={{ marginTop: 10 }}>Descrição<br/>
                <textarea value={descricao} onChange={e => setDescricao(e.target.value)} style={{ width: "100%", padding: 10, minHeight: 110 }} />
              </label>
              <div style={{ marginTop: 10 }}>
                <Botao onClick={criarChamado}>Criar</Botao>
              </div>
            </Caixa>
          )}

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 12 }}>
            <Caixa>
              <h2>Chamados</h2>
              <div style={{ display: "grid", gap: 8 }}>
                {chamados.map(c => (
                  <div key={c.id} style={{ display: "flex", justifyContent: "space-between", gap: 10, borderBottom: "1px dashed #ddd", paddingBottom: 8 }}>
                    <div>
                      <b>#{c.id}</b> {c.titulo}<br/>
                      <small style={{ color: "#666" }}>Status: {c.status} • {c.usuario.email}</small>
                    </div>
                    <Botao onClick={() => abrirChamado(c.id)}>Abrir</Botao>
                  </div>
                ))}
                {chamados.length === 0 && <div style={{ color: "#666" }}>Nenhum chamado.</div>}
              </div>
            </Caixa>

            <Caixa>
              <h2>Detalhes</h2>
              {!chamadoSelecionado ? (
                <div style={{ color: "#666" }}>Selecione um chamado.</div>
              ) : (
                <>
                  <div><b>#{chamadoSelecionado.id}</b> {chamadoSelecionado.titulo}</div>
                  <div style={{ color: "#666", marginTop: 6 }}>Status: {chamadoSelecionado.status}</div>
                  <p style={{ marginTop: 10 }}>{chamadoSelecionado.descricao}</p>

                  <h3>Respostas</h3>
                  <div style={{ display: "grid", gap: 8 }}>
                    {(chamadoSelecionado.respostas || []).map(r => (
                      <div key={r.id} style={{ border: "1px solid #eee", borderRadius: 10, padding: 10 }}>
                        <b>{r.admin.email}</b><br/>
                        <span>{r.mensagem}</span>
                      </div>
                    ))}
                    {(chamadoSelecionado.respostas || []).length === 0 && <div style={{ color: "#666" }}>Sem respostas.</div>}
                  </div>

                  {isAdmin && chamadoSelecionado.status !== "fechado" && (
                    <>
                      <h3 style={{ marginTop: 14 }}>Responder</h3>
                      <textarea value={mensagemResposta} onChange={e => setMensagemResposta(e.target.value)} style={{ width: "100%", padding: 10, minHeight: 90 }} />
                      <div style={{ display: "flex", gap: 10, marginTop: 10 }}>
                        <Botao onClick={responder}>Enviar resposta</Botao>
                        <Botao onClick={fecharChamado}>Fechar</Botao>
                      </div>
                    </>
                  )}
                </>
              )}
            </Caixa>
          </div>
        </>
      )}
    </div>
  );
}
