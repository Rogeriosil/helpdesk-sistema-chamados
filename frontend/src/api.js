const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

export function getToken() {
  return localStorage.getItem("token");
}

export function setToken(token) {
  localStorage.setItem("token", token);
}

export function setUsuario(usuario) {
  localStorage.setItem("usuario", JSON.stringify(usuario));
}

export function getUsuario() {
  try { return JSON.parse(localStorage.getItem("usuario") || "null"); }
  catch { return null; }
}

export async function api(path, { method="GET", body=null } = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data.erro || `Erro HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}
