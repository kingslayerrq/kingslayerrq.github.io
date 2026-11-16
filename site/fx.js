/* Apply the saved effects preference before paint; storage may be blocked. */
(() => {
  let fx;
  try { fx = localStorage.getItem('portfolio-fx'); } catch { /* Use system preference. */ }
  if (fx !== 'on' && fx !== 'off') {
    fx = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'off' : 'on';
  }
  document.documentElement.dataset.fx = fx;
})();
