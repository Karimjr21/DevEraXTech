// Never reflect the caller's Origin header; only allow the configured site.
function corsHeaders(_origin) {
  return {
    'Access-Control-Allow-Origin': process.env.CORS_ORIGIN || 'https://deveraxtech.com',
    Vary: 'Origin',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  };
}

function preflight(origin) {
  return {
    statusCode: 204,
    headers: corsHeaders(origin),
    body: '',
  };
}

function json(statusCode, data, origin) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
    body: JSON.stringify(data),
  };
}

module.exports = { corsHeaders, preflight, json };
