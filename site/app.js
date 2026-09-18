// Preserve links shared before project details moved off the homepage.
const legacyAnchors = {
  '#code-spire': 'slay-the-spire.html#combat',
  '#code-balatro': 'balatro.html#code-balatro',
};
if ((location.pathname.endsWith('/index.html') || location.pathname.endsWith('/')) && legacyAnchors[location.hash]) {
  location.replace(legacyAnchors[location.hash]);
}

const toggle = document.querySelector('.theme-toggle');
function updateThemeLabel() {
  const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  toggle.setAttribute('aria-label', `Switch to ${next} mode`);
  toggle.querySelector('.theme-label').textContent = `${next === 'light' ? 'Light' : 'Dark'} mode`;
}
toggle.addEventListener('click', () => {
  const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  try { localStorage.setItem('portfolio-theme', theme); } catch { /* Preference still works this visit. */ }
  updateThemeLabel();
});
updateThemeLabel();

function openLinkedDetails() {
  const target = document.getElementById(window.location.hash.slice(1));
  if (target instanceof HTMLDetailsElement) target.open = true;
}
window.addEventListener('hashchange', openLinkedDetails);
document.querySelectorAll('a[href^="#code-"]').forEach(link => {
  link.addEventListener('click', () => {
    const target = document.getElementById(link.hash.slice(1));
    if (target instanceof HTMLDetailsElement) target.open = true;
  });
});
openLinkedDetails();
document.querySelectorAll('video').forEach(video => {
  video.addEventListener('play', () => {
    document.querySelectorAll('video').forEach(other => {
      if (other !== video) other.pause();
    });
  });
});
