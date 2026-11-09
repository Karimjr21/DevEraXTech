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

const { render, ROUTES, NOT_FOUND, SITE, buildJsonLd, canonicalUrl, services, faq, business, serviceDetails, servicePath } = await import(
  pathToFileURL(path.join(ssrDir, 'entry-server.js')).href
);
const portfolio = JSON.parse(fs.readFileSync(path.join(root, 'src/data/portfolio.json'), 'utf8'));

const template = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
const today = new Date().toISOString().slice(0, 10);

// <lastmod> is the date a page's own source last changed, not the build date: a lastmod that
// moves on every deploy is ignored by Google. Falls back to today when git history is unavailable.
function lastModified(route) {
  const files = route.source
    ? [...route.source, 'src/seo.js']
    : [`pages/${route.path === '/' ? 'Home' : route.path.slice(1, 2).toUpperCase() + route.path.slice(2)}.jsx`, 'src/seo.js'];
  try {
    // Files edited but not committed yet are about to ship with today's date.
    const dirty = execFileSync('git', ['status', '--porcelain', '--', ...files], { cwd: root, encoding: 'utf8' }).trim();
    if (dirty) return today;
    const date = execFileSync('git', ['log', '-1', '--format=%cs', '--', ...files], { cwd: root, encoding: 'utf8' }).trim();
    return /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : today;
  } catch {
    return today;
  }
}

// One date per page, shared by sitemap <lastmod>, JSON-LD dateModified and the visible footer date.
const lastmod = Object.fromEntries(ROUTES.map(r => [r.path, lastModified(r)]));
const prerenderData = { services, portfolio, lastmod };

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
    `<link rel="alternate" type="application/rss+xml" title="${escAttr(SITE.name)}: services and work" href="${SITE.url}/feed.xml" />`,
    `<script type="application/ld+json" id="ld-json">${safeJson(buildJsonLd(route, { dateModified: lastmod[route.path] }))}</script>`
  ];
  return tags.filter(Boolean).join('\n    ');
}

// Markdown copy of a page's main content, served to AI agents that send `Accept: text/markdown`
// (see functions/_middleware.js). Built from the prerendered HTML so it always matches the page.
const decode = s => s.replace(/&nbsp;/g, ' ').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
function toMarkdown(route, appHtml) {
  const main = (appHtml.match(/<main[^>]*>([\s\S]*?)<\/main>/) || [, appHtml])[1]
    .replace(/<(script|style|svg|button|nav)[\s\S]*?<\/\1>/g, '')
    .replace(/<[^>]+aria-hidden="true"[^>]*>[\s\S]*?<\/(span|div)>/g, '');
  const inline = s => decode(s
    .replace(/<a [^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g, (_, href, text) => {
      const t = text.replace(/<[^>]+>/g, '').trim();
      return t ? `[${t}](${href.startsWith('/') ? SITE.url + href : href})` : '';
    })
    .replace(/<(strong|b)[^>]*>([\s\S]*?)<\/\1>/g, '**$2**')
    .replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
  const blocks = [];
  const re = /<(h[1-4]|p|li|dt|dd|summary)[^>]*>([\s\S]*?)<\/\1>/g;
  let m;
  while ((m = re.exec(main))) {
    const text = inline(m[2]);
    if (!text) continue;
    const tag = m[1];
    if (tag[0] === 'h') blocks.push(`${'#'.repeat(Number(tag[1]))} ${text}`);
    else if (tag === 'li') blocks.push(`- ${text}`);
    else if (tag === 'summary') blocks.push(`**${text}**`);
    else if (tag === 'dt') blocks.push(`**${text}:**`);
    else blocks.push(text);
  }
  const body = blocks.join('\n\n').replace(/\n\n(?=- )/g, '\n');
  return `---\ntitle: ${route.title}\nurl: ${canonicalUrl(route.path)}\ndescription: ${route.description}\nlast_updated: ${lastmod[route.path]}\n---\n\n${body}\n\n---\n\n${SITE.name}, ${business.city}, ${business.country} | ${business.phoneDisplay} | ${business.email} | ${SITE.url}/contact\n`;
}

function page(route) {
  const appHtml = render(route.path, prerenderData);
  let html = template
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${escText(route.title)}</title>`)
    .replace(/<meta name="description" content="[^"]*" \/>/, `<meta name="description" content="${escAttr(route.description)}" />`)
    .replace('<!--seo-head-->', headTags(route))
    // Keep Cloudflare's "Email Address Obfuscation" from rewriting the contact email into
    // "[email protected]" links, so crawlers and AI assistants read the real address.
    .replace('<!--app-html-->', `<!--email_off-->${appHtml}<!--/email_off-->`)
    .replace('<!--prerender-data-->', `<script type="application/json" id="__PRERENDER_DATA__">${safeJson(prerenderData)}</script>`);
  if (html.includes('<!--seo-head-->') || html.includes('<!--app-html-->')) throw new Error(`Template markers missing for ${route.path}`);
  fs.mkdirSync(path.dirname(path.join(dist, route.file)), { recursive: true });
  fs.writeFileSync(path.join(dist, route.file), html);
  if (!route.noindex) {
    const mdFile = path.join(dist, 'md', route.path === '/' ? 'index.md' : `${route.path.slice(1)}.md`);
    fs.mkdirSync(path.dirname(mdFile), { recursive: true });
    fs.writeFileSync(mdFile, toMarkdown(route, appHtml));
  }
  console.log(`prerendered ${route.path.padEnd(40)} -> dist/${route.file} (${(html.length / 1024).toFixed(1)} KB)`);
}

for (const route of ROUTES) page(route);
page(NOT_FOUND);

// sitemap.xml
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${ROUTES.map(r => `  <url>
    <loc>${canonicalUrl(r.path)}</loc>
    <lastmod>${lastmod[r.path]}</lastmod>
    <priority>${r.priority}</priority>${r.serviceId ? portfolio.filter(p => p.image && (serviceDetails[r.serviceId]?.work || []).includes(p.id)).map(p => `
    <image:image>
      <image:loc>${escText(p.image.startsWith('http') ? p.image : SITE.url + p.image)}</image:loc>
    </image:image>`).join('') : ''}${r.path === '/portfolio' ? portfolio.filter(p => p.image).map(p => `
    <image:image>
      <image:loc>${escText(p.image.startsWith('http') ? p.image : SITE.url + p.image)}</image:loc>
    </image:image>`).join('') : ''}
  </url>`).join('\n')}
</urlset>
`;
fs.writeFileSync(path.join(dist, 'sitemap.xml'), sitemap);

// robots.txt: everything is public; search and AI assistants are welcome to read and cite it.
const aiBots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Applebot-Extended', 'Bingbot'];
const robots = `# ${SITE.name}
User-agent: *
Allow: /

${aiBots.map(b => `User-agent: ${b}\nAllow: /`).join('\n\n')}

Sitemap: ${SITE.url}/sitemap.xml
`;
fs.writeFileSync(path.join(dist, 'robots.txt'), robots);

const serviceGroupNames = [...new Set(services.map(s => s.group || 'More services'))];
const serviceLine = s => `- [${s.title}](${SITE.url}${servicePath(s)}): ${s.summary} Includes: ${s.features.join('; ')}.`;

// llms.txt: a plain-language summary for AI assistants (https://llmstxt.org).
const llms = `# ${SITE.name}

> ${SITE.description}

${SITE.name} was founded in ${SITE.foundingDate} by ${SITE.founders.map(f => `${f.name} (${f.jobTitle})`).join(' and ')}. We design and build websites, apps and software that are secure by design, scalable and pixel-perfect, and we treat every project as a long-term digital asset. Most inquiries receive a response within one business day.

## At a glance

- Based in: ${business.city}, ${business.country}
- Serving clients in: ${business.areasServed.map(a => a.name).join(', ')}
- Languages: ${business.languages.map(l => l.name).join(', ')}
- Hours: ${business.hours.label}
- Phone: ${business.phoneDisplay}
- Email: ${business.email}
- Founded: ${SITE.foundingDate}; 10+ projects shipped

## Services

${serviceGroupNames.map(g => `### ${g}\n\n${services.filter(s => (s.group || 'More services') === g).map(serviceLine).join('\n')}`).join('\n\n')}

${portfolio.length ? `## Recent work

${portfolio.map(p => `### ${p.title}

${p.description}

- Client: ${p.client || p.title}
- Industry: ${p.industry || p.category}
- Location: ${p.location || business.city}
- Built with: ${(p.stack || p.tags || []).join(', ')}
- Live site: ${p.url}
${(p.services || []).length ? `- Services: ${p.services.map(id => services.find(s => s.id === id)).filter(Boolean).map(s => `[${s.title}](${SITE.url}${servicePath(s)})`).join(', ')}\n` : ''}${(p.features || []).map(f => `- ${f}`).join('\n')}`).join('\n\n')}

More projects: ${SITE.url}/portfolio

` : ''}## How we work

- Secure by design: security is embedded from architecture decisions to final QA.
- Scalable delivery: structured execution that stays reliable as scope grows.
- Design-led execution: interfaces shaped for clarity, conversion and brand consistency.
- Clear communication: transparent updates, aligned milestones and accountability.

## Frequently asked questions

${faq.map(f => `### ${f.question}\n\n${f.answer}`).join('\n\n')}

## Pages

${ROUTES.map(r => `- [${r.name}](${canonicalUrl(r.path)}): ${r.description}`).join('\n')}

## Contact

- Start a project or book a meeting: ${SITE.url}/contact
- Phone: ${business.phoneDisplay}
- Email: ${business.email}
- Hours: ${business.hours.label}
- Instagram: ${SITE.sameAs[0]}
`;
fs.writeFileSync(path.join(dist, 'llms.txt'), llms.replace('\n## Contact', `\n## Optional\n\n- [Full service details and FAQs](${SITE.url}/llms-full.txt): every service page with its audience, technology and answers to common questions.\n\n## Contact`));

// llms-full.txt: the long form, with every service page's content and FAQs.
const llmsFull = `${llms}
## Service details

${services.filter(s => serviceDetails[s.id]).map(s => {
  const d = serviceDetails[s.id];
  return `### ${d.h1}

URL: ${SITE.url}${servicePath(s)}

${d.intro.join('\n\n')}

- Includes: ${s.features.join('; ')}
- Built for: ${d.audience.join('; ')}
- Technology: ${d.stack.join('; ')}

${d.faq.map(f => `**${f.question}**\n${f.answer}`).join('\n\n')}`;
}).join('\n\n')}
`;
fs.writeFileSync(path.join(dist, 'llms-full.txt'), llmsFull);

// AI discovery endpoints: compact, machine-readable summaries for AI assistants and agents.
const aiDir = path.join(dist, 'ai');
fs.mkdirSync(aiDir, { recursive: true });
fs.writeFileSync(path.join(aiDir, 'summary.json'), JSON.stringify({
  name: SITE.name,
  url: `${SITE.url}/`,
  description: SITE.description,
  founded: SITE.foundingDate,
  founders: SITE.founders,
  location: { city: business.city, country: business.country },
  areasServed: business.areasServed.map(a => a.name),
  languages: business.languages.map(l => l.name),
  contact: { email: business.email, phone: business.phoneE164, page: `${SITE.url}/contact`, hours: business.hours.label },
  services: services.map(s => ({ name: s.title, category: s.group, url: `${SITE.url}${servicePath(s)}`, summary: s.summary, includes: s.features })),
  portfolio: portfolio.map(p => ({ name: p.title, url: p.url, category: p.category, client: p.client, year: p.year, stack: p.stack, summary: p.description })),
  llms: `${SITE.url}/llms.txt`,
  sitemap: `${SITE.url}/sitemap.xml`
}, null, 2));
const allFaq = [...faq, ...services.flatMap(s => (serviceDetails[s.id]?.faq || []).map(f => ({ ...f, service: s.title, url: `${SITE.url}${servicePath(s)}` })))];
fs.writeFileSync(path.join(aiDir, 'faq.json'), JSON.stringify(allFaq, null, 2));
fs.writeFileSync(path.join(aiDir, 'service.json'), JSON.stringify({
  name: `${SITE.name} web, app and software development services`,
  description: SITE.description,
  url: `${SITE.url}/services`,
  capabilities: services.map(s => `${s.title}: ${s.summary}`),
  provider: { name: SITE.name, url: `${SITE.url}/`, location: `${business.city}, ${business.country}`, contact: `${SITE.url}/contact` },
  areasServed: business.areasServed.map(a => a.name),
  languages: business.languages.map(l => l.name),
  howToStart: `Book a meeting at ${SITE.url}/contact, call ${business.phoneDisplay} or email ${business.email}. Replies usually within one business day.`,
  services: services.map(s => {
    const d = serviceDetails[s.id] || {};
    return {
      id: s.id,
      name: s.title,
      category: s.group,
      url: `${SITE.url}${servicePath(s)}`,
      summary: s.summary,
      includes: s.features,
      ...(d.audience ? { bestFor: d.audience } : {}),
      ...(d.stack ? { technology: d.stack } : {}),
      startProject: `${SITE.url}/contact?service=${encodeURIComponent(s.title)}`,
      lastUpdated: lastmod[servicePath(s)] || lastmod['/services']
    };
  })
}, null, 2));

// feed.xml: RSS of service pages and portfolio projects, newest first, for feed readers and AI discovery.
const rfc822 = d => new Date(`${d}T09:00:00Z`).toUTCString();
const feedItems = [
  ...portfolio.map(p => ({ title: p.title, link: `${SITE.url}/portfolio#${p.id}`, description: p.description, date: lastmod['/portfolio'], category: p.category })),
  ...ROUTES.filter(r => r.serviceId || r.path === '/maintenance').map(r => ({ title: r.title, link: canonicalUrl(r.path), description: r.description, date: lastmod[r.path], category: 'Services' }))
].sort((a, b) => b.date.localeCompare(a.date));
const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${escText(SITE.name)}: services and work</title>
    <link>${SITE.url}/</link>
    <description>${escText(SITE.description)}</description>
    <language>en</language>
    <lastBuildDate>${rfc822(feedItems[0]?.date || today)}</lastBuildDate>
    <atom:link href="${SITE.url}/feed.xml" rel="self" type="application/rss+xml" />
${feedItems.map(i => `    <item>
      <title>${escText(i.title)}</title>
      <link>${escText(i.link)}</link>
      <guid isPermaLink="true">${escText(i.link)}</guid>
      <description>${escText(i.description)}</description>
      <category>${escText(i.category)}</category>
      <pubDate>${rfc822(i.date)}</pubDate>
    </item>`).join('\n')}
  </channel>
</rss>
`;
fs.writeFileSync(path.join(dist, 'feed.xml'), feed);

fs.mkdirSync(path.join(dist, '.well-known'), { recursive: true });
fs.writeFileSync(path.join(dist, '.well-known', 'ai.txt'), `# ${SITE.name} AI policy
# Search, answer and AI assistant crawlers may read, summarize and cite this site.
User-Agent: *
Allow: /

Summary: ${SITE.url}/ai/summary.json
FAQ: ${SITE.url}/ai/faq.json
Services: ${SITE.url}/ai/service.json
Feed: ${SITE.url}/feed.xml
LLMs: ${SITE.url}/llms.txt
LLMs-Full: ${SITE.url}/llms-full.txt
Sitemap: ${SITE.url}/sitemap.xml
Contact: ${business.email}
`);

fs.rmSync(ssrDir, { recursive: true, force: true });
console.log('wrote sitemap.xml, robots.txt, llms.txt, ai/summary.json, ai/faq.json, ai/service.json, feed.xml, .well-known/ai.txt');
