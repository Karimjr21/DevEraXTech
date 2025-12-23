# DevEraX Full-Stack Project

Premium cinematic, dark-futuristic stack with gold accents.

## Frontend (React + Vite)
In `frontend`.

### Tech
React 18, Vite, TailwindCSS, Framer Motion, Three.js, React-Three-Fiber, Drei.
Enhancements: portfolio category filters + lightbox, parallax & scroll-fade hooks, optional GLTF logo loading, env-based SMTP.

### Scripts
```bash
cd frontend
npm install
npm run dev
```
Served at `http://localhost:5173`.

## Backend (Node + Express)
In `backend`.

### API Endpoints
- `POST /api/contact` -> { name, email, message }
- `GET /api/portfolio`
- `GET /api/testimonials`
- `GET /api/health`

### Scripts
```bash
cd backend
npm install
npm run dev
```
Runs at `http://localhost:4000`.

## Contact Email
Currently uses placeholder SMTP in `src/utils/mailer.js`. Replace host, auth user/pass with real credentials or environment variables.

### Resend SMTP (Node-only)
This repo includes a Nodemailer + Resend SMTP implementation in `backend/src/utils/mailer.js` and a test runner script.

Cloudflare Pages Functions (Workers runtime) cannot use Nodemailer/SMTP because they don't support raw TCP sockets.
Use the existing Resend HTTP API function (`/api/send-email`) on Cloudflare, or send via SMTP from a Node runtime (backend / Netlify / server).

### Cloudflare -> Node SMTP Bridge
If you want the Cloudflare Contact form to send via Nodemailer/SMTP, deploy the Node backend publicly and set:
- On the backend (Node): `RESEND_API_KEY` (+ optional `MAIL_FROM`, `MAIL_TO`) and `EMAIL_BRIDGE_TOKEN`.
- On Cloudflare Pages (Production env vars):
	- `EMAIL_BRIDGE_URL` = your backend endpoint URL (e.g. `https://your-backend.com/api/send-email`)
	- `EMAIL_BRIDGE_TOKEN` = same token as backend

## Frontend 3D Logo
`components/3d/Logo3D.jsx` attempts to load `/logo.glb` (place file in `frontend/public/logo.glb`). Fallback: cinematic torus knot with gold PBR + bloom + particle field + camera drift.

## Environment Variables
Copy `backend/.env.example` to `backend/.env` and supply real SMTP values.
Example:
```
PORT=4000
SMTP_HOST=smtp.mailprovider.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your_user
SMTP_PASS=your_pass
MAIL_FROM=noreply@deverax.io
MAIL_TO=team@deverax.io
```

### Serverless Email (Cloudflare Pages)
The Contact page submits to `/api/send-email` (Cloudflare Pages Function). Configure at least:
- `RESEND_API_KEY` (or `SENDGRID_API_KEY`)
- `MAIL_FROM` (and optionally `MAIL_TO`)

`MAIL_TO` defaults to `MAIL_FROM` if omitted.
Also accepted as aliases: `EMAIL_FROM`/`EMAIL_TO`, `RESEND_FROM`/`RESEND_TO`, `FROM_EMAIL`/`TO_EMAIL`, `CONTACT_FROM`/`CONTACT_TO`.

## Next Steps
- Provide actual `logo.glb` model / HDR environment map for better reflections.
- Implement masonry animation & image preloading strategy.
- Add testimonial carousel & map embed integration.
- Security hardening: rate-limit contact endpoint, validation library.

## License
Internal project.
