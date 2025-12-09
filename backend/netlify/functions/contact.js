const { preflight, json } = require('./_utils/response.cjs');

exports.handler = async (event, _context) => {
  const origin = event.headers?.origin || event.headers?.Origin;
  if (event.httpMethod === 'OPTIONS') return preflight(origin);
  if (event.httpMethod !== 'POST') {
    return json(405, { ok: false, error: 'Method Not Allowed' }, origin);
  }

  let body = {};
  try {
    if (event.body) {
      body = JSON.parse(event.body);
    }
  } catch (_e) {
    return json(400, { ok: false, error: 'Invalid JSON body' }, origin);
  }

  const { name, email, message, service, meetingDateTime } = body || {};
  if (!name || !email || !message) {
    return json(400, { ok: false, error: 'Missing required fields' }, origin);
  }

  try {
    const { sendMail } = await import('../../src/utils/mailer.js');
    const id = await sendMail({ name, email, message, service, meetingDateTime });
    return json(200, { ok: true, id }, origin);
  } catch (e) {
    let msg = 'Mail failed';
    if (e && e.message === 'SMTP_NOT_CONFIGURED') msg = 'SMTP not configured. Set backend .env or enable EMAIL_MOCK.';
    else if (e && e.message === 'SMTP_AUTH_FAILED') msg = 'SMTP authentication failed. Check SMTP_USER/SMTP_PASS (use app password for Gmail).';
    else if (e && e.message) msg = `Mail failed: ${e.message}`;
    return json(500, { ok: false, error: msg }, origin);
  }
};
