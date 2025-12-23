export async function postContact(req, res) {
  return res.status(410).json({ ok: false, error: 'GONE: email sending moved to Cloudflare Pages Function /sendEmail' });
}
