const routes = {};
export const route = (path, render) => (routes[path] = render);

export function startRouter(outlet) {
  const go = () => {
    const path = location.hash.slice(1) || '/';
    outlet.replaceChildren((routes[path] ?? routes['/'])());
    window.scrollTo(0, 0);
  };
  window.addEventListener('hashchange', go);
  go();
}

export const navigate = path => { location.hash = path; };