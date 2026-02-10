#!/usr/bin/env node
/**
 * Render LaTeX math to a standalone SVG using MathJax (tex2svg).
 * Works well for converting to PNG/JPEG via rsvg-convert/ImageMagick.
 *
 * Usage:
 *   node render_latex_svg.js "\\int_0^1 x^2\\,dx" --out out.svg
 *   node render_latex_svg.js "E=mc^2" --jpg out.jpg
 */

const fs = require('fs');
const path = require('path');

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
  console.error('Missing expression. Example: node render_latex_svg.js "E=mc^2" --out out.svg');
  process.exit(2);
}

const outSvg = getArg('--out') || getArg('--svg') || 'latex.svg';
const outPng = getArg('--png');
const outJpg = getArg('--jpg') || getArg('--jpeg');
const displayMode = hasFlag('--display');

// MathJax setup
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const {AllPackages} = require('mathjax-full/js/input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);

const tex = new TeX({packages: AllPackages});
const svg = new SVG({fontCache: 'none'});
const html = mathjax.document('', {InputJax: tex, OutputJax: svg});

// Convert
const node = html.convert(expr, {display: displayMode});
let out = adaptor.outerHTML(node);

// MathJax wraps the <svg> in an <mjx-container>. Extract the SVG root.
const m = out.match(/<svg[\s\S]*<\/svg>/m);
if (!m) {
  console.error('Failed to extract <svg> root from MathJax output');
  process.exit(1);
}
let svgText = `<?xml version="1.0" encoding="UTF-8"?>\n` + m[0];

fs.writeFileSync(outSvg, svgText, 'utf8');

// Optional rasterization
if (outPng || outJpg) {
  const { spawnSync } = require('child_process');
  const tmpPng = outPng || path.join(path.dirname(outSvg), path.basename(outSvg, '.svg') + '.png');
  const r1 = spawnSync('rsvg-convert', ['-w', '2000', '-o', tmpPng, outSvg], { stdio: 'inherit' });
  if (r1.status !== 0) process.exit(r1.status ?? 1);

  if (outJpg) {
    const r2 = spawnSync('magick', [tmpPng, '-background', 'white', '-alpha', 'remove', '-alpha', 'off', '-quality', '92', outJpg], { stdio: 'inherit' });
    if (r2.status !== 0) process.exit(r2.status ?? 1);
  }
}

console.log(outSvg);
