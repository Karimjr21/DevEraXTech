/**
 * Cloudflare Pages Function: /api/send-email
 *
 * Legacy endpoint kept for backwards compatibility.
 * Redirects POST requests to the /sendEmail Pages Function.
 */

/**
 * @typedef {Object} EmailInput
 * @property {string} name
 * @property {string} email
 * @property {string} subject
 * @property {string} message
 */

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': origin || '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
      },
    });
  }
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ success: false, error: 'Method Not Allowed' }), {
      status: 405,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': origin || '*',
      },
    });
  }

  // 308 preserves method + body
  return new Response(null, {
    status: 308,
    headers: {
      'Location': '/sendEmail',
      'Access-Control-Allow-Origin': origin || '*',
    },
  });
}
