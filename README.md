# DevEraX Website

Premium cinematic, dark-futuristic site with gold accents, hosted on Cloudflare Pages.

## Frontend (React + Vite)
In `frontend`.

### Tech
React 18, Vite, TailwindCSS, Framer Motion, Three.js, React-Three-Fiber, Drei.
Enhancements: portfolio category filters + lightbox, optional GLTF logo loading.

### Scripts
```bash
cd frontend
npm install
npm run dev
```
Served at `http://localhost:5173`.

## Cloudflare Pages Functions
In `frontend/functions`.

- `POST /sendEmail` -> sends the contact form via the Resend HTTP API
- `GET /api/portfolio`
- `GET /api/health`

Cloudflare Pages Functions run on the Workers runtime and cannot use Nodemailer/SMTP (no raw TCP sockets), so email goes through Resend.

### Environment variables (Cloudflare Pages -> Settings -> Variables and secrets)
- `RESEND_API_KEY`
- `MAIL_FROM` (must be a verified sender/domain in Resend)
- `MAIL_TO`
- `CORS_ORIGIN` (optional; only needed if another origin must call `/sendEmail`)

For local development put these in `frontend/.dev.vars` (git-ignored). Never commit real secrets.

## Security headers
`frontend/public/_headers` sets the Content-Security-Policy and other security headers for Cloudflare Pages.

## Frontend 3D Logo
`components/3d/Logo3D.jsx` attempts to load `/logo.glb` (place file in `frontend/public/logo.glb`). Fallback: cinematic torus knot with gold PBR + bloom + particle field + camera drift.

## Next Steps
- Provide actual `logo.glb` model / HDR environment map for better reflections.
- Implement masonry animation & image preloading strategy.
- Add testimonial carousel & map embed integration.

## License
Internal project.
