import { el } from '../utils.js';
import { questionText, answerText, authorName, answersOf } from '../api.js';
import { isLoggedIn } from '../auth.js';
import { answerForm } from './answerForm.js';

export function questionCard(q) {
  const answers = answersOf(q);
  const actions = el('div', { class: 'card-actions' });

  if (isLoggedIn()) {
    const toggle = el('button', { class: 'btn quiet' }, 'Write an answer');
    toggle.addEventListener('click', () => {
      toggle.replaceWith(answerForm(q.id, () => location.reload()));
    });
    actions.append(toggle);
  }

  return el('article', { class: 'card' },
    el('h2', {}, questionText(q)),
    answers.length
      ? answers.slice(0, 1).map(a => el('div', {},
          el('p', { class: 'answer' }, answerText(a)),
          el('p', { class: 'muted answer-meta' }, authorName(a))))
      : el('p', { class: 'muted' }, 'No answers yet.'),
    actions,
  );
}