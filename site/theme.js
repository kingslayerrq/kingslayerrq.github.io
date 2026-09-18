/* Apply the saved preference before paint; storage may be blocked. */
(() => {
  let theme;
  try { theme = localStorage.getItem('portfolio-theme'); } catch { /* Use system preference. */ }
  if (theme !== 'light' && theme !== 'dark') {
    theme = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  document.documentElement.dataset.theme = theme;
})();
