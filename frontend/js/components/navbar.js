import { el } from '../utils.js';
import { isLoggedIn, logout } from '../auth.js';
import { navigate } from '../router.js';

export function renderNavbar(root, { onAsk }) {
  const draw = () => {
    const authed = isLoggedIn();
    root.replaceChildren(el('nav', { class: 'nav' },
      el('a', { class: 'brand', href: '#/' }, 'Regret'),
      authed && el('a', { class: 'link', href: '#/me' }, 'Profile'),
      authed
        ? el('button', { class: 'btn', onClick: onAsk }, 'Ask a question')
        : el('a', { class: 'link', href: '#/login' }, 'Log in'),
      authed
        ? el('button', { class: 'btn quiet', onClick: () => { logout(); navigate('/'); } }, 'Log out')
        : el('a', { class: 'btn', href: '#/signup' }, 'Sign up'),
    ));
  };
  window.addEventListener('authchange', draw);
  draw();
}