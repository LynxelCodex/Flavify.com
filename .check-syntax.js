const fs = require('fs');
const src = fs.readFileSync('index.html', 'utf8');
const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let m, n = 0, bad = 0;
while ((m = re.exec(src))) {
  const attrs = m[1] || '';
  const code = m[2];
  if (/\bsrc\s*=/.test(attrs)) continue;
  n++;
  const before = src.slice(0, m.index);
  const line = before.split('\n').length;
  try {
    new Function(code);
  } catch (e) {
    bad++;
    console.log('SCRIPT #' + n + ' starting at page line ' + line + ' -> ' + e.message);
  }
}
console.log('inline scripts checked: ' + n + ', failures: ' + bad);
