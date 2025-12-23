/**
 * Cloudflare Pages Function: /sendEmail
 *
 * Cloudflare Pages Functions run on the Workers runtime (no raw TCP sockets), so SMTP/Nodemailer
 * is not supported here.
 *
 * This implementation sends email via Resend HTTP API.
 *
 * Required environment variables (Cloudflare Pages -> Variables and Secrets -> Production):
 * - RESEND_API_KEY
 * - MAIL_FROM (must be a verified sender/domain in Resend)
 * - MAIL_TO
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
  // Support both Cloudflare Pages runtime bindings (context.env)
  // and local Node-style env (process.env) for local testing.
  const processEnv = globalThis?.process?.env;
  for (const key of keys) {
    const value = env?.[key] ?? processEnv?.[key];
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

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function safeEnvPresence(env) {
  const allow = new Set([
    'RESEND_API_KEY',
    'MAIL_FROM',
    'MAIL_TO',
    'EMAIL_FROM',
    'EMAIL_TO',
    'RESEND_FROM',
    'RESEND_TO',
    'CORS_ORIGIN',
  ]);
  const presentKeys = [];
  if (env && typeof env === 'object') {
    for (const k of Object.keys(env)) {
      if (allow.has(k)) presentKeys.push(k);
    }
  }

  // process.env keys are not enumerated reliably in Workers; only check boolean presence.
  return {
    hasEnvObject: !!env && typeof env === 'object',
    presentKeys: presentKeys.sort(),
    hasRESEND_API_KEY: !!firstEnv(env, ['RESEND_API_KEY']),
    hasMAIL_FROM: !!firstEnv(env, ['MAIL_FROM', 'EMAIL_FROM', 'RESEND_FROM']),
    hasMAIL_TO: !!firstEnv(env, ['MAIL_TO', 'EMAIL_TO', 'RESEND_TO']),
  };
}

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') return preflight(origin);
  if (request.method !== 'POST') return json(405, { success: false, error: 'Method Not Allowed' }, origin);

  const resendApiKey = firstEnv(env, ['RESEND_API_KEY']);
  const mailFrom = firstEnv(env, ['MAIL_FROM', 'EMAIL_FROM', 'RESEND_FROM']);
  const mailTo = firstEnv(env, ['MAIL_TO', 'EMAIL_TO', 'RESEND_TO']);

  if (!resendApiKey) return json(500, { success: false, error: 'RESEND_API_KEY missing', debug: safeEnvPresence(env) }, origin);
  if (!mailFrom) return json(500, { success: false, error: 'MAIL_FROM missing', debug: safeEnvPresence(env) }, origin);
  if (!mailTo) return json(500, { success: false, error: 'MAIL_TO missing', debug: safeEnvPresence(env) }, origin);

  let body;
  try {
    body = await request.json();
  } catch {
    return json(400, { success: false, error: 'Invalid JSON body' }, origin);
  }

  const { valid, errors } = validateBody(body);
  if (!valid) return json(400, { success: false, errors }, origin);

  try {
    const subject = (body.subject && String(body.subject).trim())
      ? String(body.subject).trim()
      : `New Contact - ${body.service ? body.service : 'General Inquiry'} - ${body.name}`;

    const lines = [
      body.phone ? `Phone: ${body.phone}` : null,
      body.service ? `Service: ${body.service}` : null,
      body.meetingDateTime ? `Preferred Meeting: ${body.meetingDateTime}` : null,
      `Reply to: ${body.email}`,
      '',
      body.message,
    ].filter(Boolean);

    const html = `
      <div style="font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial;line-height:1.6">
        <p><strong>Name:</strong> ${escapeHtml(body.name)}</p>
        <p><strong>Email:</strong> ${escapeHtml(body.email)}</p>
        ${body.phone ? `<p><strong>Phone:</strong> ${escapeHtml(body.phone)}</p>` : ''}
        ${body.service ? `<p><strong>Service:</strong> ${escapeHtml(body.service)}</p>` : ''}
        ${body.meetingDateTime ? `<p><strong>Preferred Meeting:</strong> ${escapeHtml(body.meetingDateTime)}</p>` : ''}
        <hr/>
        <pre style="white-space:pre-wrap;font-family:inherit">${escapeHtml(body.message)}</pre>
      </div>
    `;

    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${resendApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: mailFrom,
        to: mailTo,
        subject,
        text: lines.join('\n'),
        html,
        reply_to: body.email,
      }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return json(502, { success: false, error: 'RESEND_FAILED', details: data }, origin);
    }

    return json(200, { success: true, message: 'Email sent successfully', id: data?.id }, origin);
  } catch (_e) {
    return json(502, { success: false, error: 'EMAIL_SEND_FAILED' }, origin);
  }
}
