const API_URL = '/api';

export async function fetchPortfolio() {
  const res = await fetch(`${API_URL}/portfolio`);
  return res.json();
}

export async function fetchTestimonials() {
  const res = await fetch(`${API_URL}/testimonials`);
  return res.json();
}

export async function sendContact(data) {
  const res = await fetch(`${API_URL}/send-email`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return res.json();
}
