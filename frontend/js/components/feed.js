import { el, errorBox, emptyBox } from '../utils.js';
import { api } from '../api.js';
import { questionCard } from './questionCard.js';

const PAGE_SIZE = 10;

export function renderFeed() {
  let page = 1;
  const list = el('div', { class: 'stack' });
  const more = el('button', { class: 'btn ghost block', hidden: true }, 'Load more');

  async function load() {
    more.disabled = true;
    try {
      const data = await api.feed(page);
      const items = Array.isArray(data) ? data : data.questions ?? data.items ?? [];
      items.forEach(q => list.append(questionCard(q)));
      if (!items.length && page === 1) list.append(emptyBox('No questions yet. Be the first to ask one.'));
      more.hidden = items.length < PAGE_SIZE;
      page++;
    } catch (err) {
      list.append(errorBox(err.message));
    }
    more.disabled = false;
  }

  more.addEventListener('click', load);
  load();
  return el('section', { class: 'stack' }, list, more);
}