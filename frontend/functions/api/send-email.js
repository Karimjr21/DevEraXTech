/**
 * Cloudflare Pages Function: Send Email via Resend / SendGrid, with MailChannels fallback.
 * Works on Cloudflare (no Node-only APIs). Uses `context.env` for secrets.
 *
 * Expected POST JSON: { name, email, subject, message }
 */

/**
 * @typedef {Object} EmailInput
 * @property {string} name
 * @property {string} email
 * @property {string} subject
 * @property {string} message
 */

/** Validate request body */
function validateBody(body) {
  const errors = [];
  if (!body || typeof body !== 'object') errors.push('Body must be a JSON object');
  const { name, email, subject, message } = body || {};
  if (!name || typeof name !== 'string' || !name.trim()) errors.push('Missing or invalid name');
  if (!email || typeof email !== 'string' || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) errors.push('Missing or invalid email');
  if (!subject || typeof subject !== 'string' || !subject.trim()) errors.push('Missing or invalid subject');
  if (!message || typeof message !== 'string' || !message.trim()) errors.push('Missing or invalid message');
  return { valid: errors.length === 0, errors, name, email, subject, message };
}

/** Build common JSON response */
function json(status, data, origin) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': origin || '*',
    },
  });
}

/** Preflight handler */
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

/** Send via Resend */
function firstEnv(env, keys) {
  for (const key of keys) {
    const value = env?.[key];
    if (value === undefined || value === null) continue;
    const str = typeof value === 'string' ? value : String(value);
    if (str.trim()) return str.trim();
  }
  return undefined;
}

function resolveMailConfig(env) {
  const from = firstEnv(env, ['MAIL_FROM', 'EMAIL_FROM', 'RESEND_FROM', 'FROM_EMAIL', 'CONTACT_FROM']);
  const to = firstEnv(env, ['MAIL_TO', 'EMAIL_TO', 'RESEND_TO', 'TO_EMAIL', 'CONTACT_TO', 'CONTACT_EMAIL']);
  return { from, to };
}

function safeEnvPresence(env) {
  const allow = new Set([
    'MAIL_FROM', 'MAIL_TO',
    'EMAIL_FROM', 'EMAIL_TO',
    'RESEND_FROM', 'RESEND_TO',
    'RESEND_API_KEY',
    'SENDGRID_API_KEY',
    'CORS_ORIGIN',
  ]);

  const keys = [];
  if (env && typeof env === 'object') {
    for (const k of Object.keys(env)) {
      if (allow.has(k)) keys.push(k);
    }
  }

  return {
    hasEnvObject: !!env && typeof env === 'object',
    presentKeys: keys.sort(),
    hasMAIL_FROM: !!firstEnv(env, ['MAIL_FROM']),
    hasMAIL_TO: !!firstEnv(env, ['MAIL_TO']),
    hasRESEND_API_KEY: !!firstEnv(env, ['RESEND_API_KEY']),
  };
}

async function sendWithResend(env, _from, _to, subject, html, text, replyTo) {
  const apiKey = firstEnv(env, ['RESEND_API_KEY']);
  const cfg = resolveMailConfig(env);

  // Resend supports using the demo sender in some setups, but production should use a verified sender.
  const fromAddr = cfg.from || 'DevEraX <no-reply@deveraxtech.com>';
  const toAddr = cfg.to || cfg.from;

  if (!apiKey) throw new Error('RESEND_API_KEY missing');
  if (!toAddr) {
    throw new Error(
      'EMAIL_NOT_CONFIGURED: set MAIL_TO (or EMAIL_TO/RESEND_TO). ' +
      'If this is Cloudflare Pages, make sure the variable is enabled for Pages Functions runtime and for the current environment (Production vs Preview).'
    );
  }

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: fromAddr,
      to: toAddr,
      subject,
      html,
      text,
      reply_to: replyTo || undefined,
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`RESEND_FAILED: ${res.status} ${body}`);
  }
  return await res.json();
}

/** Send via SendGrid */
async function sendWithSendGrid(env, from, to, subject, html, text) {
  const apiKey = firstEnv(env, ['SENDGRID_API_KEY']);
  const cfg = resolveMailConfig(env);
  const fromAddr = from || cfg.from || cfg.to;
  const toAddr = to || cfg.to || cfg.from;
  if (!apiKey) throw new Error('SENDGRID_API_KEY missing');
  if (!fromAddr || !toAddr) throw new Error('EMAIL_NOT_CONFIGURED: set MAIL_FROM + MAIL_TO (or EMAIL_FROM/EMAIL_TO)');
  const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: toAddr }] }],
      from: { email: fromAddr },
      subject,
      content: [
        { type: 'text/plain', value: text || '' },
        { type: 'text/html', value: html || '' },
      ],
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`SENDGRID_FAILED: ${res.status} ${body}`);
  }
  return { ok: true };
}

/** Send via MailChannels (free, native on Cloudflare) */
async function sendWithMailChannels(env, from, to, subject, html, text) {
  const cfg = resolveMailConfig(env);
  const fromAddr = from || cfg.from || cfg.to;
  const toAddr = to || cfg.to || cfg.from;
  if (!fromAddr || !toAddr) throw new Error('EMAIL_NOT_CONFIGURED: set MAIL_FROM + MAIL_TO (or EMAIL_FROM/EMAIL_TO)');
  const res = await fetch('https://api.mailchannels.net/tx/v1/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: toAddr }] }],
      from: { email: fromAddr },
      subject,
      content: [
        { type: 'text/plain', value: text || '' },
        { type: 'text/html', value: html || '' },
      ],
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`MAILCHANNELS_FAILED: ${res.status} ${body}`);
  }
  return { ok: true };
}

export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') return preflight(origin);
  if (request.method !== 'POST') return json(405, { success: false, error: 'Method Not Allowed' }, origin);

  let body;
  try {
    body = await request.json();
  } catch {
    return json(400, { success: false, error: 'Invalid JSON body' }, origin);
  }

  const { valid, errors, name, email, subject, message } = validateBody(body);
  if (!valid) return json(400, { success: false, errors }, origin);

  // Build email content
  const text = `From: ${name} <${email}>\nSubject: ${subject}\n\n${message}`;
  const html = `
    <div style="font-family:system-ui,Segoe UI,Arial;line-height:1.6">
      <p><strong>From:</strong> ${name} &lt;${email}&gt;</p>
      <p><strong>Subject:</strong> ${subject}</p>
      <hr/>
      <pre style="white-space:pre-wrap;font-family:inherit">${escapeHtml(message)}</pre>
    </div>
  `;

  try {
    let result;

    // If configured, proxy to a Node runtime (SMTP/Nodemailer) endpoint.
    // Cloudflare Workers cannot use SMTP directly.
    const bridgeUrl = firstEnv(env, ['EMAIL_BRIDGE_URL']);
    if (bridgeUrl) {
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
        return json(res.status, { success: false, error: data?.error || 'EMAIL_BRIDGE_FAILED', errors: data?.errors }, origin);
      }
      return json(200, { success: true, message: data?.message || 'Email sent successfully', result: data }, origin);
    }

    if (env?.RESEND_API_KEY) {
      // Prefer Resend when configured.
      result = await sendWithResend(env, env.MAIL_FROM, env.MAIL_TO, subject, html, text, email);
    } else if (env?.SENDGRID_API_KEY) {
      result = await sendWithSendGrid(env, env.MAIL_FROM, env.MAIL_TO, subject, html, text);
    } else {
      // Fallback: MailChannels
      result = await sendWithMailChannels(env, env.MAIL_FROM, env.MAIL_TO, subject, html, text);
    }
    return json(200, { success: true, message: 'Email sent successfully', result }, origin);
  } catch (e) {
    const message = e?.message || 'EMAIL_SEND_FAILED';
    const debug = message.startsWith('EMAIL_NOT_CONFIGURED') ? safeEnvPresence(env) : undefined;
    return json(500, { success: false, error: message, debug }, origin);
  }
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
