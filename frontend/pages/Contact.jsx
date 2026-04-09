import { useState, useMemo, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import AnimatedButton from '../components/ui/AnimatedButton';
import SectionWrapper from '../components/ui/SectionWrapper';
import { sendContact } from '../lib/api';
import { SERVICE_OPTIONS } from '../src/data/services';

const reassuranceItems = [
  {
    title: 'Fast Response Window',
    text: 'Most inquiries receive a response within one business day.'
  },
  {
    title: 'Tailored Solutions',
    text: 'Every recommendation is aligned with your goals, scale, and constraints.'
  },
  {
    title: 'Consultation-Focused',
    text: 'We start with clarity-first discovery before proposing scope or delivery.'
  },
  {
    title: 'Project Discussion Ready',
    text: 'Book a meeting for roadmap, architecture, and launch planning.'
  }
];

function formatYYYYMMDD(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function parseTimeToMinutes(hhmm) {
  const [hh, mm] = String(hhmm).split(':');
  const h = Number(hh);
  const m = Number(mm);
  if (!Number.isFinite(h) || !Number.isFinite(m)) return NaN;
  return h * 60 + m;
}

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', service: '', subject: '', message: '', meetingDate: '', meetingTime: '' });
  const [status, setStatus] = useState(null);
  const [errors, setErrors] = useState({ name: '', email: '', phone: '', service: '', message: '' });
  const [loading, setLoading] = useState(false);
  const [now, setNow] = useState(() => new Date());
  const location = useLocation();
  const fieldBase = 'contact-input w-full rounded-xl px-4 py-3.5 text-sm text-gray-100 placeholder:text-gray-500/90 outline-none transition-all duration-300';

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

  // Keep "now" fresh so same-day slots disable automatically.
  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 30_000);
    return () => clearInterval(id);
  }, []);

  const minDate = useMemo(() => formatYYYYMMDD(new Date()), []);
  const isPastSelectedDate = useMemo(() => {
    if (!form.meetingDate) return false;
    const selected = new Date(`${form.meetingDate}T00:00:00`);
    if (Number.isNaN(selected.getTime())) return false;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return selected.getTime() < today.getTime();
  }, [form.meetingDate]);

  const isTodaySelected = useMemo(() => {
    if (!form.meetingDate) return false;
    return form.meetingDate === formatYYYYMMDD(now);
  }, [form.meetingDate, now]);

  const isTimeSlotDisabled = useMemo(() => {
    const minutesNow = now.getHours() * 60 + now.getMinutes();
    return (slot) => {
      if (isPastSelectedDate) return true;
      if (!form.meetingDate) return false;
      if (!isTodaySelected) return false;
      const slotMinutes = parseTimeToMinutes(slot);
      if (!Number.isFinite(slotMinutes)) return false;
      return slotMinutes <= minutesNow;
    };
  }, [form.meetingDate, isTodaySelected, isPastSelectedDate, now]);

  // If user changes the date and the chosen time becomes invalid, clear it.
  useEffect(() => {
    if (!form.meetingTime) return;
    if (isTimeSlotDisabled(form.meetingTime)) {
      setForm(prev => ({ ...prev, meetingTime: '' }));
    }
  }, [form.meetingDate, form.meetingTime, isTimeSlotDisabled]);

  // On mount or URL change, read `service` query and pre-fill the Service field
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const svc = params.get('service');
    if (svc) {
      setForm(prev => ({ ...prev, service: svc }));
      setErrors(prev => ({ ...prev, service: '' }));
    }
  }, [location.search]);

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

    // Optional meeting selection validation
    if (isPastSelectedDate) {
      setStatus({ type: 'error', message: 'Preferred date cannot be in the past.' });
      setLoading(false);
      return;
    }
    if (form.meetingDate && form.meetingTime && isTimeSlotDisabled(form.meetingTime)) {
      setStatus({ type: 'error', message: 'Preferred time must be in the future.' });
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
        service: form.service,
        meetingDateTime: meetingDateTime || undefined,
        subject: form.subject || `Inquiry - ${form.service || 'General'}`,
        message: finalMessage,
      });
      if (res && res.success) {
        setStatus({ type: 'success', message: res.message || 'Message sent! We will get back to you shortly.' });
        setForm({ name: '', email: '', phone: '', service: '', subject: '', message: '', meetingDate: '', meetingTime: '' });
      } else {
        let msg = res?.errors ? res.errors.join(', ') : (res?.error || 'Error sending message');
        if (res?.debug && typeof res.debug === 'object') {
          msg = `${msg} | debug: ${JSON.stringify(res.debug)}`;
        }
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
    <div className="max-w-7xl mx-auto px-6 sm:px-8 pt-16 md:pt-20 pb-20 md:pb-24">
      <SectionWrapper className="space-y-10 md:space-y-12">
        <div className="max-w-3xl space-y-4">
          <h2 className="text-4xl md:text-5xl font-bold gold-gradient-text leading-[1.1]">Contact</h2>
          <p className="text-sm md:text-base text-gray-300/90 leading-relaxed max-w-2xl">
            Let&apos;s discuss your project goals, technical requirements, and the right path to a secure premium delivery.
          </p>
        </div>

        <div className="grid lg:grid-cols-[minmax(0,1.06fr)_minmax(0,0.94fr)] gap-6 xl:gap-8 items-start">
          <div className="contact-card p-6 sm:p-7 md:p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid sm:grid-cols-2 gap-4 md:gap-5">
                <div>
                  <label className="block text-sm mb-2 text-gray-300">Name</label>
                  <input
                    required
                    value={form.name}
                    onChange={e=>{ setForm({...form,name:e.target.value}); setErrors({...errors, name: ''}); }}
                    placeholder="Your full name"
                    className={`${fieldBase} ${errors.name ? 'ring-1 ring-red-500 border-red-500' : ''}`}
                  />
                  {errors.name && <p className="mt-1.5 text-xs text-red-400">{errors.name}</p>}
                </div>
                <div>
                  <label className="block text-sm mb-2 text-gray-300">Email</label>
                  <input
                    required
                    type="email"
                    value={form.email}
                    onChange={e=>{ setForm({...form,email:e.target.value}); setErrors({...errors, email: ''}); }}
                    placeholder="you@company.com"
                    className={`${fieldBase} ${errors.email ? 'ring-1 ring-red-500 border-red-500' : ''}`}
                  />
                  {errors.email && <p className="mt-1.5 text-xs text-red-400">{errors.email}</p>}
                </div>
              </div>

              <div className="grid sm:grid-cols-2 gap-4 md:gap-5">
                <div>
                  <label className="block text-sm mb-2 text-gray-300">Phone Number</label>
                  <input
                    required
                    value={form.phone}
                    onChange={e=>{ setForm({...form,phone:e.target.value}); setErrors({...errors, phone: ''}); }}
                    placeholder="+20 ..."
                    className={`${fieldBase} ${errors.phone ? 'ring-1 ring-red-500 border-red-500' : ''}`}
                  />
                  {errors.phone && <p className="mt-1.5 text-xs text-red-400">{errors.phone}</p>}
                </div>
                <div>
                  <label className="block text-sm mb-2 text-gray-300">Service</label>
                  <select
                    required
                    value={form.service}
                    onChange={e=>{ setForm({...form,service:e.target.value}); setErrors({...errors, service: ''}); }}
                    className={`${fieldBase} bg-transparent ${errors.service ? 'ring-1 ring-red-500 border-red-500' : ''}`}
                  >
                    <option value="" disabled className="bg-black">Select a service</option>
                    {SERVICE_OPTIONS.map(opt => (
                      <option key={opt} value={opt} className="bg-[#0a0a0a]">{opt}</option>
                    ))}
                  </select>
                  {errors.service && <p className="mt-1.5 text-xs text-red-400">{errors.service}</p>}
                </div>
              </div>

              <div>
                <label className="block text-sm mb-2 text-gray-300">Subject</label>
                <input
                  value={form.subject}
                  onChange={e=>setForm({...form,subject:e.target.value})}
                  placeholder="Subject (optional)"
                  className={fieldBase}
                />
              </div>

              <div className="contact-card-subpanel p-4 sm:p-5 space-y-4">
                <div className="grid md:grid-cols-2 gap-4 md:gap-5">
                  <div>
                    <label className="block text-sm mb-2 text-gray-300">Preferred Date</label>
                    <input
                      type="date"
                      min={minDate}
                      value={form.meetingDate}
                      onChange={e=>setForm({...form, meetingDate:e.target.value})}
                      className={fieldBase}
                    />
                    {isPastSelectedDate && <p className="mt-1.5 text-xs text-red-400">Preferred date cannot be in the past.</p>}
                  </div>
                  <div>
                    <label className="block text-sm mb-2 text-gray-300">Preferred Time</label>
                    <div className="flex flex-wrap gap-2.5">
                      {timeSlots.map(t => (
                        <button
                          key={t}
                          type="button"
                          disabled={isTimeSlotDisabled(t)}
                          onClick={() => {
                            if (isTimeSlotDisabled(t)) return;
                            setForm({ ...form, meetingTime: t });
                          }}
                          className={`contact-time-pill ${
                            form.meetingTime===t
                              ? 'contact-time-pill--active'
                              : isTimeSlotDisabled(t)
                                ? 'contact-time-pill--disabled'
                                : 'contact-time-pill--idle'
                          }`}
                        >{t}</button>
                      ))}
                    </div>
                    {form.meetingDate && isTodaySelected && (
                      <p className="mt-1.5 text-xs text-gray-400">Past times for today are disabled.</p>
                    )}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm mb-2 text-gray-300">Message</label>
                <textarea
                  required
                  rows={6}
                  value={form.message}
                  onChange={e=>{ setForm({...form,message:e.target.value}); setErrors({...errors, message: ''}); }}
                  placeholder="Tell us about your project goals, timeline, and priorities."
                  className={`${fieldBase} min-h-[148px] resize-y ${errors.message ? 'ring-1 ring-red-500 border-red-500' : ''}`}
                />
                {errors.message && <p className="mt-1.5 text-xs text-red-400">{errors.message}</p>}
              </div>

              <AnimatedButton
                disabled={loading || !form.name || !form.email || !form.phone || !form.service || !form.message}
                loading={loading}
                className="w-full sm:w-auto min-w-[14rem] !h-12"
              >
                Request a Meeting
              </AnimatedButton>

              {status && (
                <p className={`text-xs ${status.type==='success' ? 'text-green-400' : 'text-red-400'}`}>{status.message}</p>
              )}
            </form>
          </div>

          <aside className="contact-side-card p-6 sm:p-7 md:p-8 space-y-7">
            <div className="space-y-3">
              <p className="text-[11px] uppercase tracking-[0.2em] text-gold/70">Consultation</p>
              <h3 className="text-2xl md:text-[1.72rem] text-gold font-semibold leading-tight">Let&apos;s build something exceptional</h3>
              <p className="text-sm md:text-base text-gray-300/90 leading-relaxed">
                Share your goals and constraints. We&apos;ll help define a clear, secure, and scalable path to execution.
              </p>
            </div>

            <ul className="space-y-4">
              {reassuranceItems.map((item) => (
                <li key={item.title} className="contact-trust-row">
                  <span className="contact-trust-dot" aria-hidden />
                  <div>
                    <p className="text-sm text-gold font-medium leading-snug">{item.title}</p>
                    <p className="text-xs md:text-sm text-gray-400 mt-1 leading-relaxed">{item.text}</p>
                  </div>
                </li>
              ))}
            </ul>

            <div className="contact-side-note rounded-xl px-4 py-3 text-xs sm:text-sm text-gray-300/90">
              Meeting slots are reviewed with project context to ensure practical and focused discussions.
            </div>
          </aside>
        </div>
      </SectionWrapper>
    {status && (
      <div className={`fixed bottom-6 right-6 px-4 py-3 rounded-lg shadow-lg glass border ${status.type==='success' ? 'border-green-500 text-green-300' : 'border-red-500 text-red-300'}`}>
        {status.message}
      </div>
    )}
    </div>
  );
}
