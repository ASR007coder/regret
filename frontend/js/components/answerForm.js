import { el, errorBox } from '../utils.js';
import { api } from '../api.js';

export function answerForm(questionId, onDone) {
  const text = el('textarea', { placeholder: 'Write your answer', 'aria-label': 'Your answer', required: true });
  const msg = el('div');
  const submit = el('button', { class: 'btn', type: 'submit' }, 'Post answer');

  return el('form', {
    class: 'form',
    onSubmit: async e => {
      e.preventDefault();
      submit.disabled = true;
      try { await api.answer(questionId, text.value.trim()); onDone(); }
      catch (err) { msg.replaceChildren(errorBox(err.message)); submit.disabled = false; }
    },
  }, text, msg, submit);
}