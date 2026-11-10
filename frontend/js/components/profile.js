import { el, errorBox, emptyBox } from '../utils.js';
import { api, questionText, answerText } from '../api.js';
import { isLoggedIn } from '../auth.js';
import { navigate } from '../router.js';

const section = (title, items, render) => el('div', {},
  el('h3', { class: 'section-title' }, title),
  items.length ? el('div', { class: 'stack' }, items.map(render)) : emptyBox('Nothing here yet.'));

export function renderProfile() {
  if (!isLoggedIn()) { navigate('/login'); return el('div'); }
  const root = el('section', {}, el('p', { class: 'muted' }, 'Loading…'));

  api.me().then(me => {
    const questions = me.questions ?? [];
    const answers = me.answers ?? [];
    root.replaceChildren(
      el('div', { class: 'profile-head' },
        el('h1', {}, me.username ?? 'Your profile'),
        me.email && el('p', { class: 'muted' }, me.email)),
      section('Your questions', questions, q => el('div', { class: 'card' }, el('h2', {}, questionText(q)))),
      section('Your answers', answers, a => el('div', { class: 'card' },
        a.question && el('p', { class: 'muted' }, questionText({ question: a.question })),
        el('p', { class: 'answer' }, answerText(a)))));
  }).catch(err => root.replaceChildren(errorBox(err.message)));

  return root;
}