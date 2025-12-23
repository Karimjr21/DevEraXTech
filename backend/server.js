import express from 'express';
import cors from 'cors';
import 'dotenv/config';
import portfolioRouter from './src/routes/portfolio.js';
import testimonialsRouter from './src/routes/testimonials.js';
import { sendMail } from './src/utils/mailer.js';

const app = express();
app.use(cors({ origin: process.env.CORS_ORIGIN || 'http://localhost:5173' }));
app.use(express.json());

app.use('/api/portfolio', portfolioRouter);
app.use('/api/testimonials', testimonialsRouter);

app.post('/api/send-email', async (req, res) => {
	try {
		// Optional shared-secret auth so this endpoint isn't publicly abusable.
		// If EMAIL_BRIDGE_TOKEN is set, require: Authorization: Bearer <token>
		const expected = process.env.EMAIL_BRIDGE_TOKEN;
		if (expected) {
			const auth = req.headers.authorization || '';
			if (auth !== `Bearer ${expected}`) {
				return res.status(401).json({ success: false, error: 'Unauthorized' });
			}
		}

		const { name, email, phone, subject, message, service, meetingDateTime } = req.body || {};
		const errors = [];
		if (!name || typeof name !== 'string' || !name.trim()) errors.push('Missing or invalid name');
		if (!email || typeof email !== 'string' || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) errors.push('Missing or invalid email');
		if (!message || typeof message !== 'string' || !message.trim()) errors.push('Missing or invalid message');
		if (errors.length) return res.status(400).json({ success: false, errors });

		const extraLines = [
			phone ? `Phone: ${phone}` : null,
			subject ? `Subject: ${subject}` : null,
		].filter(Boolean);

		const composedMessage = extraLines.length
			? `${extraLines.join('\n')}\n\n${message}`
			: message;

		const id = await sendMail({
			name: String(name).trim(),
			email: String(email).trim(),
			message: composedMessage,
			service,
			meetingDateTime,
		});

		return res.status(200).json({ success: true, message: 'Email sent successfully', id });
	} catch (e) {
		return res.status(500).json({ success: false, error: e?.message || 'EMAIL_SEND_FAILED' });
	}
});

app.get('/api/health', (_req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Backend running on :${PORT}`));
