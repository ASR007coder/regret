import { el } from '../utils.js';

const EYE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>';
const EYE_OFF = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3l18 18"/><path d="M10.6 5.1A10.6 10.6 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4.2M6.6 6.6A17 17 0 0 0 2 12s3.6 7 10 7c1.8 0 3.4-.5 4.8-1.2"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>';

// Password rules: label + test. Used for the live checklist and for validation.
export const RULES = [
  ['8+ characters', v => v.length >= 8],
  ['One uppercase letter', v => /[A-Z]/.test(v)],
  ['One lowercase letter', v => /[a-z]/.test(v)],
  ['One number', v => /\d/.test(v)],
  ['One special character', v => /[^A-Za-z0-9]/.test(v)],
];

export const passwordError = v => {
  const missing = RULES.filter(([, test]) => !test(v)).map(([label]) => label.toLowerCase());
  return missing.length ? `Password needs: ${missing.join(', ')}.` : '';
};

// Password input with a show/hide (eye) button.
export function passwordField(id, label, attrs = {}) {
  const input = el('input', { id, name: id, type: 'password', required: true, maxlength: 128, ...attrs });
  const eye = el('button', { type: 'button', class: 'eye', 'aria-label': 'Show password', 'aria-pressed': 'false' });
  eye.innerHTML = EYE;

  eye.addEventListener('click', () => {
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    eye.innerHTML = show ? EYE_OFF : EYE;
    eye.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
    eye.setAttribute('aria-pressed', String(show));
  });

  const node = el('div', { class: 'field' },
    el('label', { for: id }, label),
    el('div', { class: 'pw' }, input, eye));
  return { node, input };
}