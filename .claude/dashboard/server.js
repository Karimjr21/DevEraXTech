#!/usr/bin/env node
// Agent Studio — live dashboard for the orchestrator + 6 subagents.
// Zero dependencies. Run from the project root:  node .claude/dashboard/server.js
// Then open http://localhost:4400  (change with DASHBOARD_PORT=xxxx)
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const WORK = path.join(ROOT, '.claude', 'work');
const EVENTS = path.join(WORK, 'events.jsonl');
const PORT = Number(process.env.DASHBOARD_PORT || process.argv[2] || 4400);
const HTML = path.join(__dirname, 'index.html');

const TRACKS = ['frontend', 'backend'];
const STAGES = [
  { key: 'plan', role: 'planner', file: 'plan.md', model: 'Opus 5.5' },
  { key: 'implement', role: 'implementer', file: 'impl-notes.md', model: 'Sonnet 5.5' },
  { key: 'review', role: 'reviewer', file: 'review.md', model: 'Opus 5.5' },
];
const NICK = {
  'frontend-planner': "Ostaz Ra'fat El Rassam", 'frontend-implementer': 'Hamada Pixel', 'frontend-reviewer': 'Tante Fawzeya',
  'backend-planner': 'El Mohandes Sherif', 'backend-implementer': 'Mido Async', 'backend-reviewer': 'El Shawish Atteya',
  explorer: 'Shalaby El Explorer', orchestrator: "El Me'allem Shehata",
};
const DOCS = ['00-brief.md', '01-api-contract.md', '02-file-map.md', ...TRACKS.flatMap((t) => STAGES.map((s) => `${t}-${s.file}`))];

const stat = (p) => { try { return fs.statSync(p); } catch { return null; } };
const readJSON = (p) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; } };
const readText = (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } };
const dirents = (d) => { try { return fs.readdirSync(d, { withFileTypes: true }); } catch { return []; } };

function mtimes(dir) {
  const out = [];
  const walk = (d) => dirents(d).forEach((e) => {
    const p = path.join(d, e.name);
    if (e.isDirectory()) walk(p);
    else { const s = stat(p); if (s) out.push(s.mtimeMs); }
  });
  walk(dir);
  return out;
}

function listTasks() {
  return dirents(WORK)
    .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
    .map((d) => {
      const m = mtimes(path.join(WORK, d.name));
      return { slug: d.name, updated: m.length ? Math.max(...m) : 0, created: m.length ? Math.min(...m) : 0 };
    })
    .sort((a, b) => b.updated - a.updated);
}

function readEvents(since) {
  const s = stat(EVENTS);
  if (!s) return [];
  const size = s.size;
  const start = Math.max(0, size - 512 * 1024);
  let txt = '';
  try {
    const fd = fs.openSync(EVENTS, 'r');
    const buf = Buffer.alloc(size - start);
    fs.readSync(fd, buf, 0, buf.length, start);
    fs.closeSync(fd);
    txt = buf.toString('utf8');
  } catch { return []; }
  const lines = txt.split('\n');
  if (start > 0) lines.shift();
  const out = [];
  for (const l of lines) {
    if (!l.trim()) continue;
    try { const e = JSON.parse(l); if (!since || e.ts >= since) out.push(e); } catch {}
  }
  return out;
}

// Track which subagents are running from Agent tool Pre/Post events.
function agentRuns(events) {
  const open = new Map(); // id -> {type, ts}
  const runs = {};        // type -> {count, lastStart, lastEnd, running}
  for (const e of events) {
    if (e.tool !== 'Agent' && e.tool !== 'Task') continue;
    const type = e.subagent || 'agent';
    runs[type] = runs[type] || { count: 0, lastStart: 0, lastEnd: 0, running: 0 };
    if (e.event === 'PreToolUse') {
      open.set(e.id || `${type}:${e.ts}`, { type, ts: e.ts });
      runs[type].count++;
      runs[type].lastStart = e.ts;
    } else if (e.event === 'PostToolUse') {
      let key = e.id && open.has(e.id) ? e.id : null;
      if (!key) for (const [k, v] of open) if (v.type === type) { key = k; break; }
      if (key) open.delete(key);
      runs[type].lastEnd = e.ts;
    }
  }
  for (const v of open.values()) runs[v.type].running++;
  return runs;
}

function verdictOf(text) {
  const m = text && text.match(/VERDICT:\s*(APPROVED|CHANGES REQUIRED)/i);
  return m ? m[1].toUpperCase() : null;
}

function buildState(slug) {
  const tasks = listTasks();
  const task = tasks.find((t) => t.slug === slug) || tasks[0];
  if (!task) return { tasks, task: null };

  const dir = path.join(WORK, task.slug);
  const statusDir = path.join(dir, '.status');
  const orch = readJSON(path.join(statusDir, 'orchestrator.json')) || {};
  const startedAt = Date.parse(orch.startedAt || '') || task.created - 10 * 60 * 1000;
  const events = readEvents(startedAt);
  const runs = agentRuns(events);

  const tracks = TRACKS.map((t) => {
    const stages = STAGES.map((s) => {
      const name = `${t}-${s.role}`;
      const fp = path.join(dir, `${t}-${s.file}`);
      const fs_ = stat(fp);
      const st = readJSON(path.join(statusDir, `${name}.json`)) || {};
      const run = runs[name] || { count: 0, running: 0, lastStart: 0, lastEnd: 0 };
      const text = s.key === 'review' && fs_ ? readText(fp) : null;
      const verdict = verdictOf(text);

      let state = 'pending';
      if (run.running > 0) state = 'running';
      else if (st.state === 'blocked') state = 'blocked';
      else if (fs_) state = s.key === 'review' ? (verdict === 'APPROVED' ? 'approved' : verdict ? 'changes' : 'done') : 'done';
      else if (st.state === 'running') state = 'running';

      return {
        key: s.key, name, nick: NICK[name], model: s.model, state, verdict,
        step: st.step || null,
        progress: typeof st.progress === 'number' ? st.progress : null,
        rounds: run.count,
        startedAt: run.lastStart || null,
        endedAt: run.lastEnd || null,
        updatedAt: Date.parse(st.updatedAt || '') || (fs_ ? fs_.mtimeMs : null),
        doc: fs_ ? `${t}-${s.file}` : null,
      };
    });
    return { name: t, stages, skipped: orch.skip && orch.skip.includes(t) };
  });

  const ex = runs.explorer || { count: 0, running: 0, lastStart: 0, lastEnd: 0 };
  const exStatus = readJSON(path.join(statusDir, 'explorer.json')) || {};
  const exQueries = events.filter((e) => e.subagent === 'explorer' && e.event === 'PreToolUse').map((e) => ({ ts: e.ts, q: (e.summary || '').replace(/^explorer:\s*/, '') }));
  const explorer = {
    nick: NICK.explorer, model: 'Haiku 5.5',
    state: ex.running > 0 ? 'running' : ex.count ? 'done' : 'pending',
    running: ex.running, searches: ex.count,
    step: exStatus.step || null,
    lastQuery: exQueries.length ? exQueries[exQueries.length - 1].q : null,
    recent: exQueries.slice(-4).reverse(),
    hasMap: !!stat(path.join(dir, '02-file-map.md')),
  };

  const activity = events.slice(-120).reverse().map((e) => ({
    ts: e.ts, tool: e.tool, event: e.event, summary: e.summary, subagent: e.subagent, nick: NICK[e.subagent] || null, ok: e.ok,
  }));

  return {
    now: Date.now(),
    tasks: tasks.map((t) => ({ slug: t.slug, updated: t.updated })),
    task: {
      slug: task.slug,
      title: orch.title || task.slug,
      phase: orch.phase || null,
      note: orch.note || null,
      startedAt: Date.parse(orch.startedAt || '') || task.created,
      finishedAt: Date.parse(orch.finishedAt || '') || null,
    },
    docs: DOCS.filter((d) => stat(path.join(dir, d))),
    tracks,
    explorer,
    orchestrator: NICK.orchestrator,
    toolCalls: events.filter((e) => e.event === 'PostToolUse').length,
    activity,
  };
}

const send = (res, code, body, type = 'application/json') => {
  res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(typeof body === 'string' ? body : JSON.stringify(body));
};

http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (url.pathname === '/') return send(res, 200, readText(HTML) || 'index.html missing', 'text/html; charset=utf-8');
  if (url.pathname === '/api/state') return send(res, 200, buildState(url.searchParams.get('task')));
  if (url.pathname === '/api/doc') {
    const slug = url.searchParams.get('task') || '';
    const file = url.searchParams.get('file') || '';
    if (!DOCS.includes(file) || !/^[\w.-]+$/.test(slug)) return send(res, 400, { error: 'bad request' });
    const txt = readText(path.join(WORK, slug, file));
    return txt == null ? send(res, 404, { error: 'not found' }) : send(res, 200, { file, text: txt });
  }
  send(res, 404, { error: 'not found' });
}).listen(PORT, '127.0.0.1', () => {
  console.log(`Agent Studio → http://localhost:${PORT}   (watching ${WORK})`);
});
