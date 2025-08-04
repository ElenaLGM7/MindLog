import { loadLang, setLang } from './modules/lang.js';
import { renderLogin, renderRegister, renderJournal, renderHistory } from './modules/views.js';

const app = document.getElementById('app');
let lang = localStorage.getItem('lang') || 'es';
let token = localStorage.getItem('token') || null;

export async function render(route = 'login') {
  const translations = await loadLang(lang);
  app.innerHTML = '';

  switch (route) {
    case 'login':
      renderLogin(app, translations);
      break;
    case 'register':
      renderRegister(app, translations);
      break;
    case 'journal':
      renderJournal(app, translations);
      break;
    case 'history':
      renderHistory(app, translations);
      break;
    default:
      app.innerHTML = '<p>Ruta no válida</p>';
  }
}

window.addEventListener('load', () => {
  render(token ? 'journal' : 'login');
});

export function changeLang(newLang) {
  lang = newLang;
  localStorage.setItem('lang', lang);
  render(token ? 'journal' : 'login');
}

export function setToken(newToken) {
  token = newToken;
  localStorage.setItem('token', newToken);
}
