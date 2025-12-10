import { useState, useMemo } from 'react';
import AnimatedButton from '../components/ui/AnimatedButton';
import SectionWrapper from '../components/ui/SectionWrapper';
import { sendContact } from '../lib/api';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', service: '', subject: '', message: '', meetingDate: '', meetingTime: '' });
  const [status, setStatus] = useState(null);
  const [errors, setErrors] = useState({ name: '', email: '', phone: '', service: '', message: '' });
  const [loading, setLoading] = useState(false);

  const timeSlots = useMemo(() => {
    const slots = [];
    const startHour = 8;  // 08:00
    const endHour = 18;   // 18:00
    for (let h = startHour; h <= endHour; h += 1) {
      const hours = String(h).padStart(2, '0');
      slots.push(`${hours}:00`);
    }
    return slots;
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setStatus(null);
    // Inline client-side validation matching API expectations
    const emailValid = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email);
    const nextErrors = {
      name: !form.name ? 'Name is required' : '',
      email: !emailValid ? 'Valid email is required' : '',
      phone: !form.phone ? 'Phone number is required' : '',
      service: !form.service ? 'Service is required' : '',
      message: !form.message ? 'Message is required' : '',
    };
    const hasErrors = Object.values(nextErrors).some(Boolean);
    setErrors(nextErrors);
    if (hasErrors) {
      setStatus({ type: 'error', message: 'Please fix the highlighted fields.' });
      setLoading(false);
      return;
    }
    try {
      // Combine meeting date/time into a readable string if provided
      let meetingDateTime = '';
      if (form.meetingDate && form.meetingTime) {
        const date = new Date(form.meetingDate);
        const formattedDate = date.toLocaleDateString(undefined, {
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
        meetingDateTime = `on ${formattedDate} at ${form.meetingTime}`;
      }

      // Build the final message in the required format
      const finalMessageParts = [
        `My name is ${form.name}.`,
        `I want ${form.service}.`,
      ];

      if (meetingDateTime) {
        finalMessageParts.push(`I want the meeting to be ${meetingDateTime}.`);
      }

      if (form.message) {
        finalMessageParts.push(form.message);
      }

      const finalMessage = finalMessageParts.join(' ');

      const res = await sendContact({
        name: form.name,
        email: form.email,
        phone: form.phone,
        subject: form.subject || `Inquiry - ${form.service || 'General'}`,
        message: finalMessage,
      });
      if (res && res.success) {
        setStatus({ type: 'success', message: res.message || 'Message sent! We will get back to you shortly.' });
        setForm({ name: '', email: '', service: '', subject: '', message: '', meetingDate: '', meetingTime: '' });
      } else {
        const msg = res?.errors ? res.errors.join(', ') : (res?.error || 'Error sending message');
        setStatus({ type: 'error', message: msg });
      }
    } catch (e) {
      setStatus({ type: 'error', message: 'Cannot reach backend' });
    }
    setLoading(false);
  }

  // Auto-hide toast after 3 seconds
  if (status && typeof window !== 'undefined') {
    clearTimeout(window.__contact_toast_timer);
    window.__contact_toast_timer = setTimeout(() => setStatus(null), 3000);
  }

  return (
    <div className="max-w-5xl mx-auto px-8 py-24">
      <h2 className="text-4xl font-bold mb-12 gold-gradient-text">Contact</h2>
      <SectionWrapper>
        <form onSubmit={handleSubmit} className="space-y-6 max-w-xl">
          <div>
            <label className="block text-sm mb-1 text-gray-300">Name</label>
            <input required value={form.name} onChange={e=>{ setForm({...form,name:e.target.value}); setErrors({...errors, name: ''}); }} className={`w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ${errors.name ? 'ring-red-500 border border-red-500' : 'ring-gold'}`} />
            {errors.name && <p className="mt-1 text-xs text-red-400">{errors.name}</p>}
          </div>
          <div>
            <label className="block text-sm mb-1 text-gray-300">Email</label>
            <input required type="email" value={form.email} onChange={e=>{ setForm({...form,email:e.target.value}); setErrors({...errors, email: ''}); }} className={`w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ${errors.email ? 'ring-red-500 border border-red-500' : 'ring-gold'}`} />
            {errors.email && <p className="mt-1 text-xs text-red-400">{errors.email}</p>}
          </div>
          <div>
            <label className="block text-sm mb-1 text-gray-300">Phone Number</label>
            <input required value={form.phone} onChange={e=>{ setForm({...form,phone:e.target.value}); setErrors({...errors, phone: ''}); }} className={`w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ${errors.phone ? 'ring-red-500 border border-red-500' : 'ring-gold'}`} />
            {errors.phone && <p className="mt-1 text-xs text-red-400">{errors.phone}</p>}
          </div>
          <div>
            <label className="block text-sm mb-1 text-gray-300">Service</label>
            <select
              required
              value={form.service}
              onChange={e=>setForm({...form,service:e.target.value})}
              className={`w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ${errors.service ? 'ring-red-500 border border-red-500' : 'ring-gold'} bg-transparent text-gray-200`}
            >
              <option value="" disabled className="bg-black">Select a service</option>
              {[
                'Business / Corporate Websites',
                'E-Commerce Websites',
                'Portfolio Websites',
                'Landing Pages',
              ].map(opt => (
                <option key={opt} value={opt} className="bg-[#0a0a0a]">{opt}</option>
              ))}
            </select>
            {errors.service && <p className="mt-1 text-xs text-red-400">{errors.service}</p>}
          </div>
          <div>
            <label className="block text-sm mb-1 text-gray-300">Subject</label>
            <input value={form.subject} onChange={e=>setForm({...form,subject:e.target.value})} placeholder="Subject (optional)" className="w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ring-gold" />
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm mb-1 text-gray-300">Preferred Date</label>
              <input
                type="date"
                min={new Date().toISOString().split('T')[0]}
                value={form.meetingDate}
                onChange={e=>setForm({...form, meetingDate:e.target.value})}
                className="w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ring-gold"
              />
            </div>
            <div>
              <label className="block text-sm mb-1 text-gray-300">Preferred Time</label>
              <div className="flex flex-wrap gap-2">
                {timeSlots.map(t => (
                  <button
                    key={t}
                    type="button"
                    onClick={()=>setForm({...form, meetingTime:t})}
                    className={`px-3 py-2 rounded-md text-xs border transition-all ${form.meetingTime===t ? 'border-gold bg-gold/10 text-gold' : 'border-gold/30 text-gray-300 hover:border-gold/60'}`}
                  >{t}</button>
                ))}
              </div>
            </div>
          </div>
          <div>
            <label className="block text-sm mb-1 text-gray-300">Message</label>
            <textarea required rows={5} value={form.message} onChange={e=>{ setForm({...form,message:e.target.value}); setErrors({...errors, message: ''}); }} className={`w-full glass rounded px-4 py-3 text-sm outline-none focus:ring-2 ${errors.message ? 'ring-red-500 border border-red-500' : 'ring-gold'}`} />
            {errors.message && <p className="mt-1 text-xs text-red-400">{errors.message}</p>}
          </div>
          <AnimatedButton disabled={loading || !form.name || !form.email || !form.phone || !form.service || !form.message} loading={loading}>Send Message</AnimatedButton>
          {status && (
            <p className={`text-xs ${status.type==='success' ? 'text-green-400' : 'text-red-400'}`}>{status.message}</p>
          )}
        </form>
      </SectionWrapper>
    {status && (
      <div className={`fixed bottom-6 right-6 px-4 py-3 rounded-lg shadow-lg glass border ${status.type==='success' ? 'border-green-500 text-green-300' : 'border-red-500 text-red-300'}`}>
        {status.message}
      </div>
    )}
    </div>
  );
}
