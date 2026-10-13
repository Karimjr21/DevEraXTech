/**
 * Shared branded email template. Not a route. Every outgoing email must be rendered through this module.
 *
 * Pure ES module: no imports, no Node APIs. Runs on Cloudflare Workers and in Node.
 * Email-client safe: tables + inline styles only, no <style>, no images, no web fonts, no external resources.
 */

const FONT = "'Segoe UI',Roboto,Helvetica,Arial,sans-serif";
const GOLD = '#d4af37';
const GOLD_DARK = '#8a6d12';
const GOLD_LIGHT = '#f2d17b';
const DARK = '#0a0a0a';
const CREAM = '#faf6e8';

/** Escape for HTML text and double/single-quoted attributes. null/undefined -> ''. */
export function escapeHtml(value) {
  if (value === undefined || value === null) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/** Build a safe href. Allows only https:, mailto:, tel:. Anything else returns ''.
 *  Callers never pass raw user input as `cta.href`. Use mailtoHref() for addresses. */
export function safeHref(href) {
  if (typeof href !== 'string') return '';
  const value = href.trim();
  if (/[\u0000-\u001f\u007f\s]/.test(value)) return '';
  return /^(https:|mailto:|tel:)/i.test(value) ? value : '';
}

/** mailto: link for one address. encodeURIComponent on the address, then put '@' back
 *  (so '?', '&', '#', '"' in a visitor's email cannot inject ?bcc=/&body= params). */
export function mailtoHref(address) {
  return `mailto:${encodeURIComponent(String(address ?? '')).replace(/%40/g, '@')}`;
}

function normalize(s) {
  return String(s ?? '').replace(/\r\n?/g, '\n');
}

function nl2br(s) {
  return escapeHtml(normalize(s)).replace(/\n/g, '<br>');
}

const LABEL_STYLE = `font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:${GOLD_DARK};font-weight:600`;

function visibleRows(rows) {
  return (Array.isArray(rows) ? rows : []).filter(
    r => r && (String(r.value ?? '').trim() || String(r.html ?? '').trim())
  );
}

/** Plain-text version built from the same options (used by renderBrandedEmail().text). */
export function renderPlainText(o = {}) {
  const parts = [];
  const head = [o.eyebrow ? String(o.eyebrow).toUpperCase() : '', o.title, o.intro].filter(Boolean);
  if (head.length) parts.push(head.join('\n'));
  if (o.greeting) parts.push(String(o.greeting));
  for (const p of o.paragraphs || []) if (p) parts.push(normalize(p));

  const rows = visibleRows(o.rows).filter(r => String(r.value ?? '').trim());
  if (rows.length) {
    const lines = rows.map(r => `${r.label}: ${normalize(r.value)}`);
    parts.push([o.rowsTitle, ...lines].filter(Boolean).join('\n'));
  }
  if (o.message && String(o.message.body ?? '').trim()) {
    parts.push(`${o.message.label}:\n${normalize(o.message.body)}`);
  }
  if (o.cta && safeHref(o.cta.href)) parts.push(`${o.cta.label}: ${o.cta.href.trim()}`);
  parts.push([o.footerNote, 'DevEraXTech · Secure • Scalable • Pixel-perfect'].filter(Boolean).join('\n'));

  return parts.join('\n\n').replace(/\n{3,}/g, '\n\n');
}

/**
 * Render the branded HTML email and its plain-text twin.
 * See backend-plan.md section 4.1 for the option shapes.
 * row.html is TRUSTED markup inserted verbatim. Never put user input there unescaped.
 * @returns {{ html: string, text: string }}
 */
export function renderBrandedEmail(o = {}) {
  const intro = o.intro ? String(o.intro) : '';
  const preheader = o.preheader || intro;

  const header = `
        <tr><td bgcolor="${DARK}" style="background:${DARK};padding:32px 36px;border-bottom:4px solid ${GOLD}">
          <div style="font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:${GOLD};font-weight:600">${escapeHtml(String(o.eyebrow ?? '').toUpperCase())}</div>
          <div style="font-size:26px;font-weight:700;line-height:1.25;color:${GOLD_LIGHT};margin-top:10px;word-break:break-word;overflow-wrap:anywhere">${escapeHtml(o.title)}</div>${
            intro ? `
          <div style="font-size:14px;line-height:1.6;color:#d6d6d6;margin-top:8px">${nl2br(intro)}</div>` : ''}
        </td></tr>`;

  let bodyInner = '';
  if (o.greeting) {
    bodyInner += `<div style="font-size:16px;color:#1a1a1a;margin:0 0 12px">${escapeHtml(o.greeting)}</div>`;
  }
  for (const p of o.paragraphs || []) {
    if (!p) continue;
    bodyInner += `<div style="font-size:15px;line-height:1.7;color:#3a3a3a;margin:0 0 14px">${nl2br(p)}</div>`;
  }
  const body = bodyInner
    ? `
        <tr><td style="padding:28px 36px 8px">${bodyInner}</td></tr>`
    : '';

  const rows = visibleRows(o.rows);
  let details = '';
  if (rows.length) {
    const rowsHtml = rows.map((r, i) => {
      const border = i === 0 ? '' : 'border-top:1px solid #eee3c0;';
      let value;
      if (String(r.html ?? '').trim()) {
        value = r.html;
      } else {
        const href = r.href ? safeHref(r.href) : '';
        value = href
          ? `<a href="${escapeHtml(href)}" style="color:${GOLD_DARK};text-decoration:none">${escapeHtml(r.value)}</a>`
          : escapeHtml(r.value);
      }
      return `
              <tr>
                <td width="120" style="${border}padding:10px 12px 10px 0;width:120px;vertical-align:top;${LABEL_STYLE}">${escapeHtml(r.label)}</td>
                <td style="${border}padding:10px 0;font-size:15px;line-height:1.5;color:#1a1a1a;word-break:break-word;overflow-wrap:anywhere">${value}</td>
              </tr>`;
    }).join('');
    details = `
        <tr><td style="padding:16px 36px 8px">${
          o.rowsTitle ? `
          <div style="font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:${GOLD_DARK};font-weight:700;margin-bottom:8px">${escapeHtml(o.rowsTitle)}</div>` : ''}
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="${CREAM}" style="background:${CREAM};border:1px solid #e6cf7a;border-radius:12px">
            <tr><td style="padding:6px 20px">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">${rowsHtml}
              </table>
            </td></tr>
          </table>
        </td></tr>`;
  }

  let message = '';
  if (o.message && String(o.message.body ?? '').trim()) {
    message = `
        <tr><td style="padding:20px 36px 8px">
          <div style="${LABEL_STYLE};margin-bottom:8px">${escapeHtml(o.message.label)}</div>
          <div style="background:${CREAM};border-left:3px solid ${GOLD};border-radius:6px;padding:16px 18px;font-size:15px;line-height:1.7;color:#1a1a1a;white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere">${nl2br(o.message.body)}</div>
        </td></tr>`;
  }

  let cta = '';
  const ctaHref = o.cta ? safeHref(o.cta.href) : '';
  if (ctaHref) {
    cta = `
        <tr><td style="padding:24px 36px 32px">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
            <td bgcolor="${GOLD}" style="background:${GOLD};border-radius:999px;padding:12px 24px">
              <a href="${escapeHtml(ctaHref)}" style="display:inline-block;background:${GOLD};color:${DARK};font-weight:700;font-size:14px;text-decoration:none;padding:12px 24px;border-radius:999px;word-break:break-word;overflow-wrap:anywhere">${escapeHtml(o.cta.label)}</a>
            </td>
          </tr></table>
        </td></tr>`;
  } else {
    cta = `
        <tr><td style="padding:0 36px 24px;font-size:0;line-height:0">&nbsp;</td></tr>`;
  }

  const footer = `
        <tr><td bgcolor="${DARK}" style="background:${DARK};padding:18px 36px;font-size:12px;line-height:1.6;color:#9a9a9a;text-align:center">${
          o.footerNote ? `${escapeHtml(o.footerNote)}<br>` : ''}DevEraXTech &middot; Secure &bull; Scalable &bull; Pixel-perfect
        </td></tr>`;

  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light only"><title>${escapeHtml(o.title)}</title></head>
<body style="margin:0;padding:0;background:#f2f0eb">
  <div style="display:none;max-height:0;overflow:hidden;opacity:0;mso-hide:all">${escapeHtml(preheader)}</div>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" bgcolor="#f2f0eb" style="background:#f2f0eb">
    <tr><td align="center" style="padding:24px 12px">
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" bgcolor="#ffffff" style="width:100%;max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;font-family:${FONT}">${header}${body}${details}${message}${cta}${footer}
      </table>
    </td></tr>
  </table>
</body></html>`;

  return { html, text: renderPlainText(o) };
}
