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
- `POST /api/send-email` -> email bridge endpoint (used by Cloudflare)
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
Cloudflare Pages Functions run on the Workers runtime and cannot use Nodemailer/SMTP (no raw TCP sockets).

This project sends contact email from the Pages Function `/sendEmail` via the Resend HTTP API.

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
The Contact page submits to `/sendEmail` (Cloudflare Pages Function).

Cloudflare env vars:
- `RESEND_API_KEY`
- `MAIL_FROM` (must be a verified sender/domain in Resend)
- `MAIL_TO`

Compatibility: `/api/send-email` redirects to `/sendEmail`.

## Next Steps
- Provide actual `logo.glb` model / HDR environment map for better reflections.
- Implement masonry animation & image preloading strategy.
- Add testimonial carousel & map embed integration.
- Security hardening: rate-limit contact endpoint, validation library.

## License
Internal project.
