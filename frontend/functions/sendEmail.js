/**
 * Cloudflare Pages Function: /sendEmail
 *
 * This endpoint DOES NOT send SMTP directly (Cloudflare Workers runtime cannot open TCP sockets).
 * Instead, it validates the request then proxies to a Node.js backend endpoint that sends via
 * Nodemailer + Resend SMTP.
 *
 * Required environment variables (Cloudflare Pages -> Variables and Secrets -> Production):
 * - EMAIL_BRIDGE_URL    (e.g. https://your-backend.com/api/send-email)
 * - EMAIL_BRIDGE_TOKEN  (optional, recommended)
 */

function json(status, data, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': origin || '*',
    },
  });
}

function preflight(origin) {
  return new Response('', {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': origin || '*',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    },
  });
}

function firstEnv(env, keys) {
  for (const key of keys) {
    const value = env?.[key];
    if (value === undefined || value === null) continue;
    const str = typeof value === 'string' ? value : String(value);
    if (str.trim()) return str.trim();
  }
  return undefined;
}

function validateBody(body) {
  const errors = [];
  if (!body || typeof body !== 'object') errors.push('Body must be a JSON object');
  const { name, email, phone, subject, message, service, meetingDateTime } = body || {};
  if (!name || typeof name !== 'string' || !name.trim()) errors.push('Missing or invalid name');
  if (!email || typeof email !== 'string' || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) errors.push('Missing or invalid email');
  if (phone !== undefined && phone !== null && typeof phone !== 'string') errors.push('Invalid phone');
  if (subject !== undefined && subject !== null && typeof subject !== 'string') errors.push('Invalid subject');
  if (!message || typeof message !== 'string' || !message.trim()) errors.push('Missing or invalid message');
  if (service !== undefined && service !== null && typeof service !== 'string') errors.push('Invalid service');
  if (meetingDateTime !== undefined && meetingDateTime !== null && typeof meetingDateTime !== 'string') errors.push('Invalid meetingDateTime');
  return { valid: errors.length === 0, errors };
}

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') return preflight(origin);
  if (request.method !== 'POST') return json(405, { success: false, error: 'Method Not Allowed' }, origin);

  const bridgeUrl = firstEnv(env, ['EMAIL_BRIDGE_URL']);
  if (!bridgeUrl) return json(500, { success: false, error: 'EMAIL_BRIDGE_URL missing' }, origin);

  let body;
  try {
    body = await request.json();
  } catch {
    return json(400, { success: false, error: 'Invalid JSON body' }, origin);
  }

  const { valid, errors } = validateBody(body);
  if (!valid) return json(400, { success: false, errors }, origin);

  try {
    const token = firstEnv(env, ['EMAIL_BRIDGE_TOKEN']);
    const res = await fetch(bridgeUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return json(res.status, {
        success: false,
        error: data?.error || 'EMAIL_SEND_FAILED',
        errors: data?.errors,
      }, origin);
    }

    return json(200, { success: true, message: data?.message || 'Email sent successfully', result: data }, origin);
  } catch (_e) {
    return json(502, { success: false, error: 'EMAIL_BRIDGE_UNREACHABLE' }, origin);
  }
}
