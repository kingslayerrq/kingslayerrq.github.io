const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('site/theme.js', 'utf8');
function boot(saved, light, blocked = false) {
  const document = { documentElement: { dataset: {} } };
  vm.runInNewContext(source, {
    document,
    localStorage: { getItem() { if (blocked) throw new Error('Blocked'); return saved; } },
    window: { matchMedia: () => ({ matches: light }) }
  });
  return document.documentElement.dataset.theme;
}
test('saved theme takes priority over system preference', () => {
  assert.equal(boot('dark', true), 'dark');
  assert.equal(boot('light', false), 'light');
});
test('new visits follow system preference', () => {
  assert.equal(boot(null, true), 'light');
  assert.equal(boot(null, false), 'dark');
});
test('invalid or inaccessible storage cannot break rendering', () => {
  assert.equal(boot('invalid', true), 'light');
  assert.equal(boot(null, false, true), 'dark');
});
