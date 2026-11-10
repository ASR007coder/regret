import { route, startRouter } from './router.js';
import { renderNavbar } from './components/navbar.js';
import { renderFeed } from './components/feed.js';
import { renderAuth } from './components/authForm.js';
import { renderProfile } from './components/profile.js';
import { openAskModal } from './components/askModal.js';

route('/', renderFeed);
route('/login', () => renderAuth('login'));
route('/signup', () => renderAuth('signup'));
route('/me', renderProfile);

renderNavbar(document.getElementById('navbar'), { onAsk: openAskModal });
startRouter(document.getElementById('app'));