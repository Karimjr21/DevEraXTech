const { preflight, json } = require('./_utils/response.cjs');

exports.handler = async (event, _context) => {
  const origin = event.headers?.origin || event.headers?.Origin;
  if (event.httpMethod === 'OPTIONS') return preflight(origin);
  if (event.httpMethod !== 'GET') {
    return json(405, { ok: false, error: 'Method Not Allowed' }, origin);
  }
  return json(200, { ok: true }, origin);
};
