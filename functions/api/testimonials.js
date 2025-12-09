import data from '../../backend/src/data/testimonials.json' assert { type: 'json' };

export async function onRequest(context) {
  const { request } = context;
  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': process.env.CORS_ORIGIN || '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      },
    });
  }
  if (request.method !== 'GET') {
    return new Response(JSON.stringify({ ok: false, error: 'Method Not Allowed' }), {
      status: 405,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': process.env.CORS_ORIGIN || '*',
      },
    });
  }
  try {
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': process.env.CORS_ORIGIN || '*',
      },
    });
  } catch (_e) {
    return new Response(JSON.stringify({ ok: false, error: 'DATA_FILE_NOT_FOUND' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': process.env.CORS_ORIGIN || '*',
      },
    });
  }
}
