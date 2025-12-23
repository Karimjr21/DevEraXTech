/**
 * NOTE: You must set RESEND_API_KEY as an environment variable before running.
 *
 * Install:
 *   cd backend
 *   npm install
 *
 * Run:
 *   node scripts/resend-smtp-test.mjs
 *
 * Windows (PowerShell):
 *   $env:RESEND_API_KEY = "your_api_key"
 */

import nodemailer from 'nodemailer';

async function main() {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    throw new Error('RESEND_API_KEY is not set. Please set it and try again.');
  }

  const transporter = nodemailer.createTransport({
    host: 'smtp.resend.com',
    port: 465,
    secure: true,
    auth: {
      user: 'resend',
      pass: apiKey,
    },
  });

  const info = await transporter.sendMail({
    from: 'no-reply@deveraxtech.com',
    to: 'deveraxtech@gmail.com',
    subject: 'Test Email from Resend SMTP',
    html: '<strong>Hello from SMTP!</strong>',
  });

  console.log('Email sent. Message ID:', info.messageId);
}

main().catch((err) => {
  console.error('Failed to send email:', err);
  process.exitCode = 1;
});
