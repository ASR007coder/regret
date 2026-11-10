const KEY = 'regret_token';

export const getToken = () => localStorage.getItem(KEY);
export const isLoggedIn = () => !!getToken();

export function setToken(token) {
  localStorage.setItem(KEY, token);
  window.dispatchEvent(new Event('authchange'));
}

export function logout() {
  localStorage.removeItem(KEY);
  window.dispatchEvent(new Event('authchange'));
}