import { API_BASE } from './config.js';
import { getToken } from './auth.js';

async function request(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(API_BASE + path, { method, headers, body: body && JSON.stringify(body) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const detail = data.detail ?? data.message;
    // FastAPI validation errors (422) arrive as a list of {loc, msg}.
    const text = Array.isArray(detail)
      ? detail.map(d => `${d.loc?.at(-1) ?? 'field'}: ${d.msg}`).join('. ')
      : detail;
    throw new Error(typeof text === 'string' ? text : 'Something went wrong. Try again.');
  }
  return data;
}

// One place to adjust request payloads if your backend uses different field names.
export const api = {
  signup: ({ name, dob, phone, email, password }) => request('/signup', { method: 'POST', body: { name, dob, phone, email, password } }),
  login: ({ email, password }) => request('/login', { method: 'POST', body: { email, password } }),
  feed: (page = 1) => request(`/feed?page=${page}`),
  me: () => request('/me/'),
  ask: text => request('/question', { method: 'POST', body: { question: text } }),
  answer: (id, text) => request(`/question/${id}/answer`, { method: 'POST', body: { answer: text } }),
};

// Normalizers: tolerate small differences in the response shape.
export const questionText = q => q.question ?? q.title ?? q.text ?? '';
export const answerText = a => a.answer ?? a.content ?? a.text ?? a.body ?? '';
export const authorName = x => x.author ?? x.username ?? x.user?.username ?? 'Anonymous';
export const answersOf = q => q.answers ?? (q.answer ? [q.answer] : []);