/**
 * Runs before every request on Cloudflare Pages.
 *
 * - www.deveraxtech.com/* -> 301 to https://deveraxtech.com/* (one canonical host, no duplicate content)
 * - *.pages.dev preview hosts are served with `X-Robots-Tag: noindex` so they never compete in search
 * - Requests that prefer `Accept: text/markdown` (AI agents) get the page's Markdown copy
 *   from /md/<path>.md, written at build time by scripts/prerender.mjs
 */
const CANONICAL_HOST = 'deveraxtech.com';

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === `www.${CANONICAL_HOST}`) {
    url.hostname = CANONICAL_HOST;
    url.protocol = 'https:';
    url.port = '';
    return Response.redirect(url.toString(), 301);
  }

  const accept = context.request.headers.get('Accept') || '';
  const isPage = context.request.method === 'GET' && !url.pathname.startsWith('/api/') && !/\.[a-z0-9]+$/i.test(url.pathname);
  const mdPath = `/md${url.pathname === '/' ? '/index' : url.pathname.replace(/\/+$/, '')}.md`;

  if (isPage && /text\/markdown/i.test(accept)) {
    const md = await context.env.ASSETS.fetch(new URL(mdPath, url.origin));
    if (md.ok) {
      return new Response(md.body, {
        status: 200,
        headers: {
          'Content-Type': 'text/markdown; charset=utf-8',
          'Vary': 'Accept',
          'Cache-Control': 'public, max-age=300',
          ...(url.hostname.endsWith('.pages.dev') ? { 'X-Robots-Tag': 'noindex' } : {})
        }
      });
    }
  }

  const response = await context.next();

  if (isPage && response.status === 200 && (response.headers.get('Content-Type') || '').includes('text/html')) {
    const html = new Response(response.body, response);
    html.headers.append('Vary', 'Accept');
    html.headers.set('Link', `<${mdPath}>; rel="alternate"; type="text/markdown"`);
    if (url.hostname.endsWith('.pages.dev')) html.headers.set('X-Robots-Tag', 'noindex');
    return html;
  }

  if (url.hostname.endsWith('.pages.dev')) {
    const tagged = new Response(response.body, response);
    tagged.headers.set('X-Robots-Tag', 'noindex');
    return tagged;
  }

  return response;
}
