export async function onRequest(context) {
  const { request, env } = context;
  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      },
    });
  }
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ ok: false, error: 'Method Not Allowed' }), {
      status: 405,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
      },
    });
  }

  let body = {};
  try {
    body = await request.json();
  } catch (_e) {
    return new Response(JSON.stringify({ ok: false, error: 'Invalid JSON body' }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
      },
    });
  }

  const { name, email, message, service, meetingDateTime } = body || {};
  if (!name || !email || !message) {
    return new Response(JSON.stringify({ ok: false, error: 'Missing required fields' }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
      },
    });
  }

  try {
    const required = ['SMTP_HOST','SMTP_PORT','SMTP_SECURE','SMTP_USER','SMTP_PASS','MAIL_FROM','MAIL_TO','EMAIL_MOCK'];
    for (const k of required) {
      if (env && env[k] !== undefined) {
        // Map to process.env for existing mailer
        process.env[k] = String(env[k]);
      }
    }
    const module = await import('../../backend/src/utils/mailer.js');
    const id = await module.sendMail({ name, email, message, service, meetingDateTime });
    return new Response(JSON.stringify({ ok: true, id }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
      },
    });
  } catch (e) {
    let msg = 'Mail failed';
    if (e && e.message === 'SMTP_NOT_CONFIGURED') msg = 'SMTP not configured. Set backend .env or enable EMAIL_MOCK.';
    else if (e && e.message === 'SMTP_AUTH_FAILED') msg = 'SMTP authentication failed. Check SMTP_USER/SMTP_PASS (use app password for Gmail).';
    else if (e && e.message) msg = `Mail failed: ${e.message}`;
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': env?.CORS_ORIGIN || '*',
      },
    });
  }
}
