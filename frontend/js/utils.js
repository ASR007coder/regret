// Tiny DOM helper: el('div', {class: 'x', onClick: fn}, child, 'text')
export function el(tag, props = {}, ...kids) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(props)) {
    if (v == null || v === false) continue;
    if (k.startsWith('on')) node.addEventListener(k.slice(2).toLowerCase(), v);
    else if (k === 'class') node.className = v;
    else node.setAttribute(k, v === true ? '' : v);
  }
  node.append(...kids.flat().filter(k => k != null && k !== false));
  return node;
}

export const errorBox = msg => el('p', { class: 'error', role: 'alert' }, msg);
export const emptyBox = msg => el('p', { class: 'empty' }, msg);