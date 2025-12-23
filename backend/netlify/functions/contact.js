const { preflight, json } = require('./_utils/response.cjs');

exports.handler = async (event, _context) => {
  const origin = event.headers?.origin || event.headers?.Origin;
  if (event.httpMethod === 'OPTIONS') return preflight(origin);

  return json(410, { ok: false, error: 'GONE: Netlify function not used (use Cloudflare /sendEmail + Node bridge)' }, origin);
};
