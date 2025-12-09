import express from 'express';
import cors from 'cors';
import 'dotenv/config';
import portfolioRouter from './src/routes/portfolio.js';
import testimonialsRouter from './src/routes/testimonials.js';

const app = express();
app.use(cors({ origin: 'http://localhost:5173' }));
app.use(express.json());

app.use('/api/portfolio', portfolioRouter);
app.use('/api/testimonials', testimonialsRouter);

app.get('/api/health', (_req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Backend running on :${PORT}`));
