const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function login(email, password) {
  const form = new URLSearchParams();
  form.append('username', email);
  form.append('password', password);
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form,
  });
  if (!res.ok) throw new Error('Login failed');
  return res.json();
}

export async function register(email, password, isAdmin = false) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, is_admin: isAdmin }),
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
}

export async function uploadDocument(file, token) {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_URL}/documents/upload`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function listDocuments(token) {
  const res = await fetch(`${API_URL}/documents/list`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('List failed');
  return res.json();
}

export async function chatQuery(message, token) {
  const res = await fetch(`${API_URL}/chat/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error('Chat failed');
  return res.json();
} 