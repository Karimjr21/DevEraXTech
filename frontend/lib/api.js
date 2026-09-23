const API_URL = '/api';

async function getJSON(path) {
  const res = await fetch(`${API_URL}${path}`, { headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(`Request failed (${res.status})`);
  return res.json();
}

export async function fetchPortfolio() {
  const data = await getJSON('/portfolio');
  return Array.isArray(data) ? data : [];
}

export async function fetchServices() {
  const data = await getJSON('/services');
  return Array.isArray(data) ? data : [];
}

export async function sendContact(data) {
  const res = await fetch('/sendEmail', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}
