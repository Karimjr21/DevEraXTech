function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin || process.env.CORS_ORIGIN || '*',
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
