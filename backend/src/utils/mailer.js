import nodemailer from 'nodemailer';

export async function sendMail({ name, email, message, service, meetingDateTime }) {
  if (process.env.EMAIL_MOCK === 'true') {
    return 'mocked-dev-id';
  }

  // Resend SMTP shortcut (recommended when deploying Node-based functions)
  // Uses: host smtp.resend.com, port 465, user resend, pass RESEND_API_KEY
  const resendApiKey = process.env.RESEND_API_KEY;
  const host = process.env.SMTP_HOST;
  const useResendSmtp = !!resendApiKey && (!host || host === 'smtp.resend.com');

  const user = useResendSmtp ? 'resend' : process.env.SMTP_USER;
  const pass = useResendSmtp ? resendApiKey : process.env.SMTP_PASS;
  const effectiveHost = useResendSmtp ? 'smtp.resend.com' : host;

  if (!effectiveHost || !user || !pass) {
    throw new Error('SMTP_NOT_CONFIGURED');
  }

  let transporter;
  if (useResendSmtp) {
    transporter = nodemailer.createTransport({
      host: 'smtp.resend.com',
      port: 465,
      secure: true,
      auth: { user: 'resend', pass: resendApiKey },
    });
  } else if ((effectiveHost || '').includes('gmail.com') || process.env.SMTP_SERVICE === 'gmail') {
    transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: { user, pass }
    });
  } else {
    transporter = nodemailer.createTransport({
      host: effectiveHost,
      port: parseInt(process.env.SMTP_PORT || '587', 10),
      secure: process.env.SMTP_SECURE === 'true',
      auth: { user, pass },
      tls: { rejectUnauthorized: false }
    });
  }

  // Verify connection (gives clearer errors like invalid login)
  try {
    await transporter.verify();
  } catch (e) {
    if (e && /Invalid|authentication|auth/i.test(e.message || '')) {
      throw new Error('SMTP_AUTH_FAILED');
    }
    throw e;
  }

  const lines = [
    `Message: ${message}`,
    service ? `Service: ${service}` : null,
    meetingDateTime ? `Preferred Meeting: ${meetingDateTime}` : null,
    `Reply to: ${email}`
  ].filter(Boolean);

  const info = await transporter.sendMail({
    from: process.env.MAIL_FROM || (useResendSmtp ? 'no-reply@deveraxtech.com' : user),
    to: process.env.MAIL_TO || (useResendSmtp ? 'deveraxtech@gmail.com' : user),
    subject: `New Contact - ${service ? service : 'General Inquiry'} - ${name}`,
    text: lines.join('\n')
  });
  return info.messageId;
}
