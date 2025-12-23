export async function onRequest(context) {
  const { request, env } = context;
  const origin = env?.CORS_ORIGIN || '*';

  if (request.method === 'OPTIONS') {
    return new Response('', {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
      },
    });
  }

  return new Response(
    JSON.stringify({
      ok: false,
      error: 'GONE: use /sendEmail',
    }),
    {
      status: 410,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': origin,
      },
    }
  );
}
