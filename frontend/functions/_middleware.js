/**
 * Runs before every request on Cloudflare Pages.
 *
 * - www.deveraxtech.com/* -> 301 to https://deveraxtech.com/* (one canonical host, no duplicate content)
 * - *.pages.dev preview hosts are served with `X-Robots-Tag: noindex` so they never compete in search
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

  const response = await context.next();

  if (url.hostname.endsWith('.pages.dev')) {
    const tagged = new Response(response.body, response);
    tagged.headers.set('X-Robots-Tag', 'noindex');
    return tagged;
  }

  return response;
}
