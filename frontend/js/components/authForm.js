import { el, errorBox } from '../utils.js';
import { api } from '../api.js';
import { setToken } from '../auth.js';
import { navigate } from '../router.js';
import { passwordField, passwordError, RULES } from './passwordField.js';

const field = (id, label, attrs = {}) =>
  el('div', { class: 'field' },
    el('label', { for: id }, label),
    el('input', { id, name: id, type: 'text', required: true, ...attrs }));

export function renderAuth(mode) {
  const signup = mode === 'signup';
  const msg = el('div');
  const submit = el('button', { class: 'btn', type: 'submit' }, signup ? 'Create account' : 'Log in');

  const pw = passwordField('password', 'Password', { autocomplete: signup ? 'new-password' : 'current-password' });
  const confirm = signup && passwordField('confirm', 'Confirm password', { autocomplete: 'new-password' });
  const rules = signup && el('ul', { class: 'rules', 'aria-label': 'Password requirements' },
    RULES.map(([label]) => el('li', {}, label)));
  const match = signup && el('p', { class: 'error', hidden: true }, 'Passwords do not match.');

  // Live feedback while typing (signup only: login never blocks on complexity).
  const check = () => {
    if (!signup) return;
    const v = pw.input.value;
    [...rules.children].forEach((li, i) => li.classList.toggle('ok', RULES[i][1](v)));
    pw.input.setCustomValidity(passwordError(v));
    const mismatch = confirm.input.value !== '' && confirm.input.value !== v;
    match.hidden = !mismatch;
    confirm.input.setCustomValidity(mismatch ? 'Passwords do not match.' : '');
  };
  pw.input.addEventListener('input', check);
  confirm && confirm.input.addEventListener('input', check);

  const form = el('form', {
    class: 'form',
    onSubmit: async e => {
      e.preventDefault();
      submit.disabled = true;
      const d = Object.fromEntries(new FormData(form));
      d.email = d.email.trim().toLowerCase();
      try {
        if (signup) await api.signup({ ...d, name: d.name.trim() }); // confirm is never sent
        const res = await api.login({ email: d.email, password: d.password });
        setToken(res.access_token ?? res.token);
        navigate('/');
      } catch (err) {
        msg.replaceChildren(errorBox(err.message));
        submit.disabled = false;
      }
    },
  },
    signup && field('name', 'Full name', { minlength: 2, maxlength: 100, autocomplete: 'name' }),
    field('email', 'Email', { type: 'email', autocomplete: 'email' }),
    signup && field('dob', 'Date of birth', { type: 'date', max: new Date().toISOString().slice(0, 10) }),
    signup && field('phone', 'Phone', { type: 'tel', maxlength: 15, autocomplete: 'tel' }),
    pw.node,
    rules,
    confirm && confirm.node,
    match,
    msg, submit);

  return el('section', { class: 'auth' },
    el('h1', {}, signup ? 'Create your account' : 'Welcome back'),
    form,
    el('p', { class: 'muted auth-switch' },
      signup ? 'Already have an account? ' : 'New here? ',
      el('a', { href: signup ? '#/login' : '#/signup' }, signup ? 'Log in' : 'Sign up')));
}