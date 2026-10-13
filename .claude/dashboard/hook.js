#!/usr/bin/env node
// Claude Code hook: appends one line per tool call to .claude/work/events.jsonl
// so the dashboard can show which agents are running and what they're doing.
// It never blocks or fails the tool call: every error is swallowed and it always exits 0.
const fs = require('fs');
const path = require('path');

let raw = '';
process.stdin.on('data', (c) => (raw += c));
process.stdin.on('end', () => {
  try {
    const e = JSON.parse(raw || '{}');
    const root = process.env.CLAUDE_PROJECT_DIR || e.cwd || process.cwd();
    const dir = path.join(root, '.claude', 'work');
    fs.mkdirSync(dir, { recursive: true });
    const ti = e.tool_input || {};
    const rec = {
      ts: Date.now(),
      event: e.hook_event_name || null,
      tool: e.tool_name || null,
      id: e.tool_use_id || null,
      session: e.session_id || null,
      agent: e.agent_type || null,
      subagent: ti.subagent_type || null,
      summary: summarize(e.tool_name, ti, root),
    };
    if (e.hook_event_name === 'PostToolUse') {
      const r = e.tool_response;
      rec.ok = !(r && typeof r === 'object' && (r.is_error || r.error));
    }
    fs.appendFileSync(path.join(dir, 'events.jsonl'), JSON.stringify(rec) + '\n');
  } catch (_) {
    /* never break the agent */
  }
  process.exit(0);
});

function rel(p, root) {
  if (!p || typeof p !== 'string') return '';
  return p.startsWith(root) ? p.slice(root.length).replace(/^[\\/]/, '') : p;
}

function summarize(tool, ti, root) {
  const cut = (s, n = 140) => (s && s.length > n ? s.slice(0, n - 1) + '…' : s || '');
  switch (tool) {
    case 'Bash':
      return cut(ti.description || ti.command);
    case 'Read':
    case 'Write':
    case 'Edit':
    case 'NotebookEdit':
      return rel(ti.file_path || ti.notebook_path, root);
    case 'Agent':
    case 'Task':
      return cut(`${ti.subagent_type || 'agent'}: ${ti.description || ''}`);
    case 'Skill':
      return ti.skill || '';
    case 'Grep':
      return cut(`/${ti.pattern || ''}/ ${rel(ti.path, root)}`);
    case 'Glob':
      return cut(ti.pattern);
    case 'WebSearch':
      return cut(ti.query);
    case 'WebFetch':
      return cut(ti.url);
    default:
      return '';
  }
}
