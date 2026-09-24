// Renders each .dc.html artboard to a PNG by expanding its template in plain Chromium
// (holes, sc-for, sc-if, dc-import), since the canvas runtime isn't available locally.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const SRC = process.argv[2] || path.join(__dirname, "screens");
const OUT = process.argv[3] || path.join(__dirname, "screenshots");

function parse(file) {
  const html = fs.readFileSync(path.join(SRC, file), 'utf8');
  const xdc = html.match(/<x-dc>([\s\S]*?)<\/x-dc>/)[1];
  const helmet = (xdc.match(/<helmet>([\s\S]*?)<\/helmet>/) || [, ''])[1];
  const body = xdc.replace(/<helmet>[\s\S]*?<\/helmet>/, '');
  const script = html.match(/<script type="text\/x-dc" data-dc-script data-props='([\s\S]*?)'>([\s\S]*?)<\/script>/);
  const props = JSON.parse(script[1].replace(/&#39;/g, "'").replace(/&amp;/g, '&'));
  return { helmet, body, code: script[2], props };
}

const EXPANDER = `
function makeVals(code, props) {
  class DCLogic { constructor() { this.props = {}; this.state = {}; } setState(o) { Object.assign(this.state, o); } }
  const Component = new Function('DCLogic', code + '; return Component;')(DCLogic);
  const c = new Component();
  for (const k in props) if (k[0] !== '$' && props[k] && 'default' in props[k]) c.props[k] = props[k].default;
  return c.renderVals();
}
function get(path, scope) {
  path = path.trim();
  if (path === 'true') return true; if (path === 'false') return false;
  if (/^-?\\d+(\\.\\d+)?$/.test(path)) return Number(path);
  return path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), scope);
}
function interp(str, scope) {
  const whole = str.match(/^\\{\\{([^}]+)\\}\\}$/);
  if (whole) return get(whole[1], scope);
  return str.replace(/\\{\\{([^}]+)\\}\\}/g, (_, p) => { const v = get(p, scope); return v == null ? '' : v; });
}
function expand(parent, scope, imports) {
  for (const node of Array.from(parent.childNodes)) {
    if (node.nodeType === 3) { if (node.nodeValue.includes('{{')) node.nodeValue = interp(node.nodeValue, scope); continue; }
    if (node.nodeType !== 1) continue;
    const tag = node.localName;
    if (tag === 'sc-for') {
      const list = interp(node.getAttribute('list'), scope) || [];
      const as = node.getAttribute('as');
      const frag = document.createDocumentFragment();
      list.forEach((item, i) => {
        const holder = document.createElement('div');
        for (const ch of Array.from(node.childNodes)) holder.appendChild(ch.cloneNode(true));
        expand(holder, Object.assign({}, scope, { [as]: item, $index: i }), imports);
        while (holder.firstChild) frag.appendChild(holder.firstChild);
      });
      node.replaceWith(frag);
      continue;
    }
    if (tag === 'sc-if') {
      if (interp(node.getAttribute('value'), scope)) {
        expand(node, scope, imports);
        node.replaceWith(...Array.from(node.childNodes));
      } else node.remove();
      continue;
    }
    if (tag === 'dc-import') {
      const holder = document.createElement('div');
      holder.innerHTML = imports[node.getAttribute('name')] || '';
      node.replaceWith(...Array.from(holder.childNodes));
      continue;
    }
    for (const a of Array.from(node.attributes)) {
      if (/^on[A-Z]/.test(a.name) || /^on/i.test(a.name) && a.value.includes('{{')) { node.removeAttribute(a.name); continue; }
      if (a.value.includes('{{')) {
        const v = interp(a.value, scope);
        if (v === false || v == null) node.removeAttribute(a.name); else node.setAttribute(a.name, String(v));
      }
    }
    expand(node, scope, imports);
  }
}
window.renderBoard = function (b, imports) {
  const vals = makeVals(b.code, b.props);
  const root = document.getElementById('root');
  root.innerHTML = b.body;
  expand(root, vals, imports);
  return root.innerHTML;
};
`;

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', proxy: { server: process.env.HTTPS_PROXY || process.env.https_proxy } });
  const files = fs.readdirSync(SRC).filter((f) => f.endsWith('.dc.html'));
  const boards = Object.fromEntries(files.map((f) => [f.replace('.dc.html', ''), parse(f)]));
  const rendered = {};
  const order = Object.keys(boards).sort((a, b) => (a === 'Main') - (b === 'Main')); // Main imports others, so last
  fs.mkdirSync(OUT, { recursive: true });
  for (const name of order) {
    const b = boards[name];
    const w = b.props.$preview.width, h = b.props.$preview.height;
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2, ignoreHTTPSErrors: true });
    const helmet = b.helmet.replace(/<\/?helmet>/g, '');
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8">${helmet}<style>body{margin:0}</style></head><body><div id="root"></div><script>${EXPANDER}</script></body></html>`);
    rendered[name] = await page.evaluate(([bb, imp]) => window.renderBoard(bb, imp), [b, rendered]);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1500); await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(OUT, name + '.png'), clip: { x: 0, y: 0, width: w, height: h } });
    await page.close();
    console.log('rendered', name);
  }
  await browser.close();
})();
