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

// Only send CORS headers when CORS_ORIGIN is configured. The site itself calls
// /sendEmail same-origin, so no CORS header is needed and other sites are refused.
function corsHeaders(origin) {
  return origin ? { 'Access-Control-Allow-Origin': origin, Vary: 'Origin' } : {};
}

function json(status, data, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}

function preflight(origin) {
  return new Response(null, {
    status: 204,
    headers: {
      ...corsHeaders(origin),
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
    },
  });
}

const MAX_BODY_BYTES = 20_000;
const MAX_LENGTHS = {
  name: 200,
  email: 254,
  phone: 50,
  subject: 200,
  service: 200,
  meetingDateTime: 200,
  message: 5000,
};

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
  for (const [field, max] of Object.entries(MAX_LENGTHS)) {
    const value = body?.[field];
    if (typeof value === 'string' && value.length > max) errors.push(`${field} is too long (max ${max} characters)`);
  }
  return { valid: errors.length === 0, errors };
}

// Collapse CR/LF and other control characters in single-line fields (subject, reply-to, etc.).
function singleLine(str) {
  return String(str).replace(/[\u0000-\u001f\u007f]+/g, ' ').trim();
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN;

  if (request.method === 'OPTIONS') return preflight(origin);
  if (request.method !== 'POST') return json(405, { success: false, error: 'Method Not Allowed' }, origin);

  const contentLength = Number(request.headers.get('Content-Length') || 0);
  if (contentLength > MAX_BODY_BYTES) return json(413, { success: false, error: 'Payload Too Large' }, origin);

  const resendApiKey = firstEnv(env, ['RESEND_API_KEY']);
  const mailFrom = firstEnv(env, ['MAIL_FROM', 'EMAIL_FROM', 'RESEND_FROM']);
  const mailTo = firstEnv(env, ['MAIL_TO', 'EMAIL_TO', 'RESEND_TO']);

  if (!resendApiKey || !mailFrom || !mailTo) {
    return json(500, { success: false, error: 'EMAIL_SERVICE_UNAVAILABLE' }, origin);
  }

  let body;
  try {
    const raw = await request.text();
    if (raw.length > MAX_BODY_BYTES) return json(413, { success: false, error: 'Payload Too Large' }, origin);
    body = JSON.parse(raw);
  } catch {
    return json(400, { success: false, error: 'Invalid JSON body' }, origin);
  }

  // Honeypot: the contact form has a hidden "website" field that people never fill in.
  // Bots that do are told the message was sent, but nothing is emailed.
  if (body && typeof body === 'object' && typeof body.website === 'string' && body.website.trim()) {
    return json(200, { success: true, message: 'Email sent successfully' }, origin);
  }

  const { valid, errors } = validateBody(body);
  if (!valid) return json(400, { success: false, errors }, origin);

  try {
    const subject = singleLine((body.subject && String(body.subject).trim())
      ? String(body.subject).trim()
      : `New Contact - ${body.service ? body.service : 'General Inquiry'} - ${body.name}`);

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
        reply_to: singleLine(body.email),
      }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return json(502, { success: false, error: 'EMAIL_SEND_FAILED' }, origin);
    }

    return json(200, { success: true, message: 'Email sent successfully', id: data?.id }, origin);
  } catch (_e) {
    return json(502, { success: false, error: 'EMAIL_SEND_FAILED' }, origin);
  }
}
