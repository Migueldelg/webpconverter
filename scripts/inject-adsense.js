#!/usr/bin/env node
/**
 * Inserta automáticamente el script de Google AdSense en el <head>
 * de TODAS las páginas HTML del sitio, incluidas las que se creen en el futuro.
 *
 * Se ejecuta solo en un sitio: aquí. Para cambiar el client ID de AdSense,
 * edítalo únicamente en la constante ADSENSE_CLIENT de abajo.
 *
 * Se ejecuta automáticamente en cada deploy de Vercel (ver vercel.json ->
 * buildCommand). También puedes ejecutarlo a mano en local con:
 *   node scripts/inject-adsense.js
 */
const fs = require('fs');
const path = require('path');

const ADSENSE_CLIENT = 'ca-pub-7213402290601307';
const LOADER_SNIPPET =
  '  <!-- GOOGLE ADSENSE -->\n' +
  `  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}" crossorigin="anonymous"></script>\n`;
// NOTA: Auto Ads está activado desde el panel de AdSense (Anuncios > Por
// sitio). NO añadir aquí un push({ enable_page_level_ads: true }) manual:
// el propio script loader ya activa Auto Ads cuando está confirmado en el
// panel, y el push manual duplicado causa el error en consola
// "Only one 'enable_page_level_ads' allowed per page" que bloquea los anuncios.

const ROOT = path.resolve(__dirname, '..');
const IGNORE_DIRS = new Set(['node_modules', '.git', '.github', '.idea', 'scripts', '.vercel']);

function findHtmlFiles(dir) {
  let results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (IGNORE_DIRS.has(entry.name)) continue;
      results = results.concat(findHtmlFiles(path.join(dir, entry.name)));
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      results.push(path.join(dir, entry.name));
    }
  }
  return results;
}

let updated = 0;
let skipped = 0;

for (const file of findHtmlFiles(ROOT)) {
  let html = fs.readFileSync(file, 'utf8');

  if (!html.includes('</head>')) {
    console.warn(`AVISO: ${file} no tiene </head>, se omite`);
    continue;
  }

  let changed = false;

  // Quita cualquier push manual de enable_page_level_ads que haya quedado
  // de una versión anterior del script (duplica la Auto Ads del panel).
  const pushBlockRe = /\s*<!-- GOOGLE ADSENSE - AUTO ADS -->\s*\n\s*<script>\s*\n\s*\(adsbygoogle[\s\S]*?<\/script>\n?/;
  if (pushBlockRe.test(html)) {
    html = html.replace(pushBlockRe, '\n');
    changed = true;
  }

  if (!html.includes(ADSENSE_CLIENT)) {
    html = html.replace('</head>', `${LOADER_SNIPPET}</head>`);
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(file, html, 'utf8');
    updated++;
    console.log(`AdSense actualizado en ${path.relative(ROOT, file)}`);
  } else {
    skipped++;
  }
}

console.log(`\nHecho: ${updated} pagina(s) actualizada(s), ${skipped} ya lo tenian.`);
