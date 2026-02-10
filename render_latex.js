#!/usr/bin/env node
/**
 * Render a LaTeX math expression to SVG (and optionally PNG/JPEG).
 *
 * Usage:
 *   node render_latex.js "\\int_0^1 x^2 dx" --out out.svg
 *   node render_latex.js "E=mc^2" --png out.png
 *
 * Notes:
 * - Uses KaTeX (no TeX install).
 * - For raster outputs, requires: rsvg-convert + ImageMagick (magick).
 */

const fs = require('fs');
const path = require('path');
const katex = require('katex');

function getArg(name) {
  const i = process.argv.indexOf(name);
  if (i === -1) return null;
  return process.argv[i + 1] ?? null;
}

function hasFlag(name) {
  return process.argv.includes(name);
}

const expr = process.argv.slice(2).find(a => !a.startsWith('-'));
if (!expr) {
  console.error('Missing expression. Example: node render_latex.js "E=mc^2" --out out.svg');
  process.exit(2);
}

const outSvg = getArg('--out') || (hasFlag('--svg') ? getArg('--svg') : null);
const outPng = getArg('--png');
const outJpg = getArg('--jpg') || getArg('--jpeg');

const displayMode = hasFlag('--display');
const throwOnError = !hasFlag('--no-throw');

let svg;
try {
  svg = katex.renderToString(expr, {
    output: 'mathml', // we'll wrap via HTML+CSS; but KaTeX can output HTML+MathML
    displayMode,
    throwOnError,
  });
} catch (e) {
  console.error(String(e));
  process.exit(1);
}

// KaTeX's renderToString outputs HTML. For a self-contained SVG, we can use KaTeX's internal
// build by requiring the 'katex/contrib/auto-render' isn't useful here.
// Instead, use KaTeX's 'katex.renderToString' with output:'html' and embed into a foreignObject.
// This keeps things simple and renders well in browsers; for PNG, we rely on rsvg which may not
// support foreignObject. So we also provide a plain HTML output pathway.
//
// Practical approach: output HTML snippet + KaTeX CSS, then (optionally) user can screenshot.
// For fully portable SVG without foreignObject we'd need katex-svg support; not included.

const html = katex.renderToString(expr, { displayMode, throwOnError });

const cssPath = require.resolve('katex/dist/katex.min.css');
const css = fs.readFileSync(cssPath, 'utf8');

const svgDoc = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
  <defs>
    <style type="text/css"><![CDATA[
${css}
    ]]></style>
  </defs>
  <foreignObject x="0" y="0" width="100%" height="100%">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-size:32px; padding:10px;">
      ${html}
    </div>
  </foreignObject>
</svg>
`;

const writePath = outSvg || 'latex.svg';
fs.writeFileSync(writePath, svgDoc, 'utf8');

// Optional rasterization (best-effort)
if (outPng || outJpg) {
  const { spawnSync } = require('child_process');
  const tmpPng = outPng || path.join(path.dirname(writePath), path.basename(writePath, '.svg') + '.png');

  const r1 = spawnSync('rsvg-convert', ['-w', '2000', '-o', tmpPng, writePath], { stdio: 'inherit' });
  if (r1.status !== 0) process.exit(r1.status ?? 1);

  if (outJpg) {
    const r2 = spawnSync('magick', [tmpPng, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', '-quality', '92', outJpg], { stdio: 'inherit' });
    if (r2.status !== 0) process.exit(r2.status ?? 1);
  }
}

console.log(writePath);
