import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

export function getPortfolio(_req, res) {
  try {
    const file = fileURLToPath(new URL('../data/portfolio.json', import.meta.url));
    const data = JSON.parse(fs.readFileSync(file, 'utf-8'));
    res.json(data);
  } catch (e) {
    res.status(500).json({ ok: false, error: 'DATA_FILE_NOT_FOUND' });
  }
}
