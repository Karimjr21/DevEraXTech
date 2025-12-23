/**
 * Deprecated duplicate handler.
 *
 * Cloudflare Pages Functions for this project live under `frontend/functions`.
 * This endpoint only redirects to the new `/sendEmail` function.
 */

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
      },
    });
  }

  return new Response(null, {
    status: 308,
    headers: {
      Location: '/sendEmail',
      'Access-Control-Allow-Origin': origin,
    },
  });
}
