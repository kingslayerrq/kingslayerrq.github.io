const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('site/fx.js', 'utf8');
function boot(saved, reducedMotion, blocked = false) {
  const document = { documentElement: { dataset: {} } };
  vm.runInNewContext(source, {
    document,
    localStorage: { getItem() { if (blocked) throw new Error('Blocked'); return saved; } },
    window: { matchMedia: () => ({ matches: reducedMotion }) }
  });
  return document.documentElement.dataset.fx;
}
test('saved effects preference takes priority over the system setting', () => {
  assert.equal(boot('on', true), 'on');
  assert.equal(boot('off', false), 'off');
});
test('new visits respect reduced-motion', () => {
  assert.equal(boot(null, true), 'off');
  assert.equal(boot(null, false), 'on');
});
test('invalid or inaccessible storage cannot break rendering', () => {
  assert.equal(boot('invalid', true), 'off');
  assert.equal(boot(null, false, true), 'on');
});
