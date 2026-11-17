// Preserve links shared before project details moved off the homepage.
const legacyAnchors = {
  '#code-spire': 'slay-the-spire.html#combat',
  '#code-balatro': 'balatro.html#code-balatro',
};
if ((location.pathname.endsWith('/index.html') || location.pathname.endsWith('/')) && legacyAnchors[location.hash]) {
  location.replace(legacyAnchors[location.hash]);
}

const root = document.documentElement;
const effectsOff = () => root.dataset.fx === 'off' || window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// CRT effects toggle: scanlines and ambient animation.
const fxToggle = document.querySelector('.fx-toggle');
function syncFx() {
  const on = root.dataset.fx !== 'off';
  fxToggle.setAttribute('aria-pressed', String(on));
  fxToggle.querySelector('.fx-state').textContent = on ? 'On' : 'Off';
}
fxToggle.addEventListener('click', () => {
  root.dataset.fx = root.dataset.fx === 'off' ? 'on' : 'off';
  try { localStorage.setItem('portfolio-fx', root.dataset.fx); } catch { /* Preference still works this visit. */ }
  syncFx();
});
syncFx();

// Local time in the status bar.
const clock = document.querySelector('[data-clock]');
if (clock) {
  const tick = () => {
    const now = new Date();
    clock.textContent = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  };
  tick();
  setInterval(tick, 15000);
}

// Visual-novel dialogue box. Without JavaScript every line is simply listed.
const dialogue = document.querySelector('[data-dialogue]');
if (dialogue) {
  const lines = [...dialogue.querySelectorAll('.dialogue-lines p')];
  const texts = lines.map(line => line.textContent);
  const next = dialogue.querySelector('.dialogue-next');
  let index = 0;
  let timer = null;
  const finish = () => {
    clearInterval(timer);
    timer = null;
    lines[index].textContent = texts[index];
    lines[index].classList.remove('is-typing');
  };
  const show = target => {
    if (timer) finish();
    index = target;
    lines.forEach((line, n) => { line.hidden = n !== index; });
    next.firstChild.textContent = index === lines.length - 1 ? 'Replay ' : 'Next ';
    if (effectsOff()) return;
    const line = lines[index];
    let shown = 0;
    line.textContent = '';
    line.classList.add('is-typing');
    timer = setInterval(() => {
      shown += 1;
      line.textContent = texts[index].slice(0, shown);
      if (shown >= texts[index].length) finish();
    }, 20);
  };
  next.addEventListener('click', () => {
    if (timer) finish();
    else show((index + 1) % lines.length);
  });
  dialogue.classList.add('is-live');
  next.hidden = false;
  show(0);
}

// Project filters on the menu page.
const filters = document.querySelector('[data-filters]');
if (filters) {
  let track = 'all';
  const items = [...document.querySelectorAll('[data-track]')];
  const groups = [...document.querySelectorAll('[data-group]')];
  const count = filters.querySelector('[data-filter-count]');
  const apply = () => {
    let visible = 0;
    items.forEach(item => {
      const match = track === 'all' || item.dataset.track === track;
      item.hidden = !match;
      if (match) visible += 1;
    });
    groups.forEach(group => { group.hidden = !group.querySelector('[data-track]:not([hidden])'); });
    count.textContent = `${visible} of ${items.length} shown`;
  };
  filters.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', () => {
      track = button.dataset.filterTrack;
      button.parentElement.querySelectorAll('button').forEach(other => {
        other.setAttribute('aria-pressed', String(other === button));
      });
      apply();
    });
  });
  filters.hidden = false;
  apply();
}

// Recipe pages: open linked code disclosures and keep one video playing at a time.
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

// Jukebox: the Spotify player loads only after the visitor opens it, and nothing autoplays.
const jukebox = document.querySelector('[data-jukebox]');
if (jukebox) {
  const panel = jukebox.querySelector('.jukebox-panel');
  const link = jukebox.querySelector('.jukebox-toggle');
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = link.className;
  toggle.innerHTML = link.innerHTML;
  toggle.setAttribute('aria-controls', panel.id);
  toggle.setAttribute('aria-expanded', 'false');
  link.replaceWith(toggle);
  toggle.addEventListener('click', () => {
    if (!panel.querySelector('iframe')) {
      const frame = document.createElement('iframe');
      frame.title = 'Spotify player';
      frame.loading = 'lazy';
      frame.allow = 'autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture';
      frame.src = `https://open.spotify.com/embed/album/${encodeURIComponent(jukebox.dataset.jukebox)}?theme=0`;
      panel.querySelector('.jukebox-body').append(frame);
      panel.hidden = false;
      panel.classList.add('is-min');
    }
    const open = panel.classList.toggle('is-min') === false;
    panel.inert = !open;
    toggle.setAttribute('aria-expanded', String(open));
  });
}
