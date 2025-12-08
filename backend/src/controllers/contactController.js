import { sendMail } from '../utils/mailer.js';

export async function postContact(req, res) {
  const { name, email, message, service, meetingDateTime } = req.body || {};
  if (!name || !email || !message) return res.status(400).json({ ok: false, error: 'Missing required fields' });
  try {
    const id = await sendMail({ name, email, message, service, meetingDateTime });
    res.json({ ok: true, id });
  } catch (e) {
    let msg = 'Mail failed';
    if (e && e.message === 'SMTP_NOT_CONFIGURED') msg = 'SMTP not configured. Set backend .env or enable EMAIL_MOCK.';
    else if (e && e.message === 'SMTP_AUTH_FAILED') msg = 'SMTP authentication failed. Check SMTP_USER/SMTP_PASS (use app password for Gmail).';
    else if (e && e.message) msg = `Mail failed: ${e.message}`;
    res.status(500).json({ ok: false, error: msg });
  }
}
