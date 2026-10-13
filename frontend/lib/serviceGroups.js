export const GROUP_ORDER = ['Websites & Stores', 'Apps & Software', 'Growth & Support'];
export const GROUP_INTROS = {
  'Websites & Stores': 'Corporate sites, online stores and campaign pages, designed and built end to end.',
  'Apps & Software': 'Web, mobile and desktop software, plus the AI and payment integrations that connect it to how you work.',
  'Growth & Support': 'Care, optimization and design support for products that are live or about to be.'
};
export const slugify = s => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// [{ name, id, intro, items: [{ ...service, index }] }]. index is the global 0-based position (continuous numbering).
export function groupServices(list = []) {
  const map = new Map();
  list.forEach((s, index) => {
    const name = s.group || 'More Services';
    if (!map.has(name)) map.set(name, []);
    map.get(name).push({ ...s, index });
  });
  const names = [...map.keys()].sort((a, b) => {
    const ia = GROUP_ORDER.indexOf(a), ib = GROUP_ORDER.indexOf(b);
    return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
  });
  return names.map(name => ({ name, id: slugify(name), intro: GROUP_INTROS[name] || '', items: map.get(name) }));
}

// Balanced card grid: base 1 col, sm 2 cols, lg 6-col track. No lone card on the last row.
// Literal class strings below so Tailwind (content glob added for ./lib) generates them.
export function cardSpanClass(count, i) {
  const classes = [];
  if (count % 2 === 1 && i === count - 1) classes.push('sm:col-span-2');
  const r = count % 3;
  const tail = r === 2 ? 2 : (r === 1 && count >= 4 ? 4 : 0);
  classes.push(i >= count - tail ? 'lg:col-span-3' : 'lg:col-span-2');
  return classes.join(' ');
}
export const serviceHref = s => s.link || `/services#${s.id}`;
