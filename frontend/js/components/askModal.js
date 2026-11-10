import { el, errorBox } from '../utils.js';
import { api } from '../api.js';

export function openAskModal() {
  const text = el('textarea', { placeholder: 'What would you like to ask?', 'aria-label': 'Your question', required: true });
  const msg = el('div');
  const post = el('button', { class: 'btn', type: 'submit' }, 'Post question');
  const dialog = el('dialog', {},
    el('form', {
      class: 'form', style: 'margin:0',
      onSubmit: async e => {
        e.preventDefault();
        post.disabled = true;
        try { await api.ask(text.value.trim()); dialog.close(); location.hash = '/'; location.reload(); }
        catch (err) { msg.replaceChildren(errorBox(err.message)); post.disabled = false; }
      },
    },
      el('h3', {}, 'Ask a question'),
      text, msg,
      el('div', { class: 'modal-actions' },
        el('button', { class: 'btn ghost', type: 'button', onClick: () => dialog.close() }, 'Cancel'), post)));

  dialog.addEventListener('close', () => dialog.remove());
  document.body.append(dialog);
  dialog.showModal();
}