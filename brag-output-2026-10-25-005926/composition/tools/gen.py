import json, sys, html as H
OUT = sys.argv[1]
# Trimmed from DevEraXTech/frontend/pages/Home.jsx (hero), re-wrapped to a narrow print width.
CODE = [
    ('<p className="eyebrow text-gold">', None),
    ('  ENGINEERED EXCELLENCE', 'sup'),
    ('</p>', None),
    ('<h1 className="gold-gradient-text">', None),
    ('  We build premium web &amp; app experiences', 'h1'),
    ('</h1>', None),
    ('<p className="text-gray-300">', None),
    ('  Modern, secure and scalable solutions,', 'body'),
    ('  from prototypes to production.', 'body'),
    ('</p>', None),
    ('<AnimatedButton to="/contact">', None),
    ('  Request a Meeting', 'b1'),
    ('</AnimatedButton>', None),
    ('<AnimatedButton variant="outline" to="/services">', None),
    ('  View Our Services', 'b2'),
    ('</AnimatedButton>', None),
    ('<span>Secure • Scalable • Pixel-perfect</span>', 'tri'),
]
TOP, LH, LEFT, CW = 676, 37, 130, 15.6

def hl(src):
    """tiny JSX highlighter → spans"""
    out, i = [], 0
    s = src
    import re
    tok = re.compile(r'(</?[A-Za-z0-9]+|/?>|[A-Za-z]+(?==)|"[^"]*"|=)')
    pos = 0
    for m in tok.finditer(s):
        if m.start() > pos:
            out.append(f'<span class="tx">{H.escape(s[pos:m.start()])}</span>')
        t = m.group(0)
        cls = 'tg' if t.startswith('<') or t.endswith('>') else ('st' if t.startswith('"') else ('pu' if t == '=' else 'at'))
        out.append(f'<span class="{cls}">{H.escape(t)}</span>')
        pos = m.end()
    if pos < len(s):
        out.append(f'<span class="tx">{H.escape(s[pos:])}</span>')
    return ''.join(out)

lines_html, typing = [], []
t = 0.22
for i, (src, tok) in enumerate(CODE):
    vis = src.replace('&amp;', '&') if False else src
    n = len(src.replace('&amp;', '&amp;'))
    top = TOP + LH * i
    lines_html.append(f'<div class="ln" style="top:{top}px"><span class="num">{i+1}</span>'
                      f'<span class="code" id="sc-c{i}">{hl(src)}</span></div>')
    if i >= 3:
        dur = max(0.1, n * 0.0064)
        typing.append([i, round(t, 3), round(dur, 3), n, top])
        t += dur + 0.028
print('typing ends', t, file=sys.stderr)

# deterministic star field (the site's hero has one)
seed = 7
def rnd():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed / 2147483648
stars = []
for _ in range(80):
    x, y = rnd() * 1080, 560 + rnd() * 820
    s = 1.5 + rnd() * 2.5
    o = 0.18 + rnd() * 0.5
    stars.append(f'<i style="left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px;opacity:{o:.2f}"></i>')

html = open(sys.argv[2]).read()
html = (html.replace('__LINES__', '\n'.join(lines_html)).replace('__STARS__', ''.join(stars))
        .replace('__TYPING__', json.dumps(typing)).replace('__CW__', str(CW)).replace('__LEFT__', str(LEFT)))
open(OUT, 'w').write(html)
# keypress times for the root
print(json.dumps([round(x[1], 2) for x in typing]))
