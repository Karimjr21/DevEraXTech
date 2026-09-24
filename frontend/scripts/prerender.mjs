// Build-time prerender: turns the single-page app into one static HTML file per route,
// so search engines, social previews and AI crawlers get real content and per-page
// <head> tags without running JavaScript. Also writes sitemap.xml, robots.txt and llms.txt.
//
// Runs after `vite build` (client) and `vite build --ssr` (server entry); see package.json.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const ssrDir = path.join(root, '.ssr');

const { render, ROUTES, NOT_FOUND, SITE, buildJsonLd, canonicalUrl, services, faq, homeFaq, business } = await import(
  pathToFileURL(path.join(ssrDir, 'entry-server.js')).href
);
const portfolio = JSON.parse(fs.readFileSync(path.join(root, 'src/data/portfolio.json'), 'utf8'));

const template = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
const manifestPath = path.join(dist, '.vite', 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const prerenderData = { services, portfolio };
const today = new Date().toISOString().slice(0, 10);

// <lastmod> is the date a page's own source last changed, not the build date: a lastmod that
// moves on every deploy is ignored by Google. Falls back to today when git history is unavailable.
function pageSource(route) {
  return `pages/${route.path === '/' ? 'Home' : route.path.slice(1, 2).toUpperCase() + route.path.slice(2)}.jsx`;
}

function lastModified(route) {
  const files = [pageSource(route), 'src/seo.js'];
  try {
    const date = execFileSync('git', ['log', '-1', '--format=%cs', '--', ...files], { cwd: root, encoding: 'utf8' }).trim();
    return /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : today;
  } catch {
    return today;
  }
}

const escAttr = s => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const escText = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// JSON inside <script> must not contain "</script>" or "<!--".
const safeJson = obj => JSON.stringify(obj).replace(/</g, '\\u003c');

function headTags(route) {
  const url = route.noindex ? `${SITE.url}${route.path}` : canonicalUrl(route.path);
  const tags = [
    route.noindex ? null : `<link rel="canonical" href="${escAttr(url)}" />`,
    `<meta name="robots" content="${route.noindex ? 'noindex, follow' : 'index, follow, max-image-preview:large'}" />`,
    `<meta property="og:type" content="website" />`,
    `<meta property="og:site_name" content="${escAttr(SITE.name)}" />`,
    `<meta property="og:locale" content="${escAttr(SITE.locale)}" />`,
    `<meta property="og:title" content="${escAttr(route.title)}" />`,
    `<meta property="og:description" content="${escAttr(route.description)}" />`,
    `<meta property="og:url" content="${escAttr(url)}" />`,
    `<meta property="og:image" content="${escAttr(SITE.image)}" />`,
    `<meta property="og:image:width" content="1200" />`,
    `<meta property="og:image:height" content="630" />`,
    `<meta property="og:image:alt" content="${escAttr(SITE.imageAlt)}" />`,
    `<meta name="twitter:card" content="summary_large_image" />`,
    `<meta name="twitter:title" content="${escAttr(route.title)}" />`,
    `<meta name="twitter:description" content="${escAttr(route.description)}" />`,
    `<meta name="twitter:image" content="${escAttr(SITE.image)}" />`,
    `<script type="application/ld+json" id="ld-json">${safeJson(buildJsonLd(route))}</script>`
  ];
  return tags.filter(Boolean).join('\n    ');
}

// <link rel="modulepreload"> for the route's page chunk (see routes/pages.js) and the shared
// chunks it imports, so the browser fetches them alongside the main script instead of after it.
function pagePreloads(route) {
  const source = route.path === '/404' ? 'pages/NotFound.jsx' : pageSource(route);
  const files = new Set();
  const visit = key => {
    const chunk = manifest[key];
    if (!chunk || chunk.isEntry || files.has(chunk.file)) return;
    files.add(chunk.file);
    (chunk.imports || []).forEach(visit);
  };
  if (!manifest[source]) throw new Error(`No chunk for ${source} in the Vite manifest`);
  visit(source);
  return [...files].map(file => `<link rel="modulepreload" crossorigin href="/${file}">`).join('\n    ');
}

async function page(route) {
  const appHtml = await render(route.path, prerenderData);
  let html = template
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${escText(route.title)}</title>`)
    .replace(/<meta name="description" content="[^"]*" \/>/, `<meta name="description" content="${escAttr(route.description)}" />`)
    .replace('<!--seo-head-->', headTags(route))
    .replace('</head>', `  ${pagePreloads(route)}\n  </head>`)
    // Keep Cloudflare's "Email Address Obfuscation" from rewriting the contact email into
    // "[email protected]" links, so crawlers and AI assistants read the real address.
    .replace('<!--app-html-->', `<!--email_off-->${appHtml}<!--/email_off-->`)
    .replace('<!--prerender-data-->', `<script type="application/json" id="__PRERENDER_DATA__">${safeJson(prerenderData)}</script>`);
  if (html.includes('<!--seo-head-->') || html.includes('<!--app-html-->')) throw new Error(`Template markers missing for ${route.path}`);
  fs.writeFileSync(path.join(dist, route.file), html);
  console.log(`prerendered ${route.path.padEnd(11)} -> dist/${route.file} (${(html.length / 1024).toFixed(1)} KB)`);
}

for (const route of ROUTES) await page(route);
await page(NOT_FOUND);
fs.rmSync(path.join(dist, '.vite'), { recursive: true, force: true });

// sitemap.xml
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${ROUTES.map(r => `  <url>
    <loc>${canonicalUrl(r.path)}</loc>
    <lastmod>${lastModified(r)}</lastmod>
    <priority>${r.priority}</priority>
  </url>`).join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(dist, 'sitemap.xml'), sitemap);

// robots.txt: everything is public; search and AI assistants are welcome to read and cite it.
const aiBots = [
  'GPTBot', 'OAI-SearchBot', 'ChatGPT-User',
  'ClaudeBot', 'Claude-SearchBot', 'Claude-User',
  'PerplexityBot', 'Perplexity-User',
  'Google-Extended', 'GoogleOther', 'Bingbot',
  'Applebot', 'Applebot-Extended',
  'Amazonbot', 'meta-externalagent', 'DuckAssistBot', 'MistralAI-User', 'CCBot'
];
const robots = `# ${SITE.name}
User-agent: *
Allow: /

${aiBots.map(b => `User-agent: ${b}\nAllow: /`).join('\n\n')}

Sitemap: ${SITE.url}/sitemap.xml
`;
fs.writeFileSync(path.join(dist, 'robots.txt'), robots);

// llms.txt: a plain-language summary for AI assistants (https://llmstxt.org).
const llms = `# ${SITE.name}

> ${SITE.description}

${SITE.name} was founded in ${SITE.foundingDate} by ${SITE.founders.map(f => `${f.name} (${f.jobTitle})`).join(' and ')}. We design and build websites that are secure by design, scalable and pixel-perfect, and we treat every project as a long-term digital asset. Most inquiries receive a response within one business day.

## At a glance

- Based in: ${business.city}, ${business.country}
- Serving clients in: ${business.areasServed.map(a => a.name).join(', ')}
- Languages: ${business.languages.map(l => l.name).join(', ')}
- Hours: ${business.hours.label}
- Phone: ${business.phoneDisplay}
- Email: ${business.email}
- Founded: ${SITE.foundingDate}; 10+ projects shipped

## Services

${services.map(s => `- [${s.title}](${SITE.url}/services#${s.id}): ${s.summary} Includes: ${s.features.join('; ')}.`).join('\n')}

## How we work

- Secure by design: security is embedded from architecture decisions to final QA.
- Scalable delivery: structured execution that stays reliable as scope grows.
- Design-led execution: interfaces shaped for clarity, conversion and brand consistency.
- Clear communication: transparent updates, aligned milestones and accountability.

## Frequently asked questions

${[...faq, ...homeFaq].map(f => `### ${f.question}\n\n${f.answer}`).join('\n\n')}

## Pages

${ROUTES.map(r => `- [${r.name}](${canonicalUrl(r.path)}): ${r.description}`).join('\n')}

## Contact

- Start a project or book a meeting: ${SITE.url}/contact
- Phone: ${business.phoneDisplay}
- Email: ${business.email}
- Hours: ${business.hours.label}
- Instagram: ${SITE.sameAs[0]}
`;
fs.writeFileSync(path.join(dist, 'llms.txt'), llms);

fs.rmSync(ssrDir, { recursive: true, force: true });
console.log('wrote sitemap.xml, robots.txt, llms.txt');
