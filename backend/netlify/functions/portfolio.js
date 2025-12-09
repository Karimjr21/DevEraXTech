const { preflight, json } = require('./_utils/response.cjs');

// Require JSON so bundler includes it in the function bundle
let portfolioData;
try {
  portfolioData = require('../../src/data/portfolio.json');
} catch (e) {
  portfolioData = null;
}

exports.handler = async (event, _context) => {
  const origin = event.headers?.origin || event.headers?.Origin;
  if (event.httpMethod === 'OPTIONS') return preflight(origin);
  if (event.httpMethod !== 'GET') {
    return json(405, { ok: false, error: 'Method Not Allowed' }, origin);
  }
  try {
    if (!portfolioData) throw new Error('DATA_FILE_NOT_FOUND');
    return json(200, portfolioData, origin);
  } catch (e) {
    return json(500, { ok: false, error: 'DATA_FILE_NOT_FOUND' }, origin);
  }
};
