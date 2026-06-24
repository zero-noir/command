const API_BASE = (import.meta.env.VITE_API_BASE_URL ?? import.meta.env.VITE_API_BASE ?? 'http://localhost:8000').replace(/\/$/, '');
const API_PREFIX = (import.meta.env.VITE_STARTUP_COMMAND_API_PREFIX ?? '/api/v1/startup-command/api').replace(/^\/?/, '/').replace(/\/$/, '');

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const route = path.startsWith('/') ? path : `/${path}`;
  const res = await fetch(`${API_BASE}${API_PREFIX}${route}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(detail || `Request failed with status ${res.status}`);
  }

  return res.json() as Promise<T>;
}

export type Agent = {
  id: string;
  title: string;
  domain: string;
  path: string;
  excerpt: string;
  source: string;
  capability_tags: string[];
  good_for: string[];
};

export type ComposeResponse = {
  objective: string;
  ai_mode: string;
  selected_agents: Agent[];
  workflow_steps: { title: string; owner: string; action: string; output: string }[];
  operating_risks: string[];
  success_metrics: string[];
  handoff_brief: string;
};

export type OpsResponse = {
  ai_mode: string;
  title: string;
  summary: string;
  decisions: string[];
  actions: string[];
  risks: string[];
  metrics: string[];
  next_brief: string;
};

export const api = {
  health: () => request<any>('/health'),
  agents: () => request<Agent[]>('/agents'),
  compose: (payload: { objective: string; agent_ids: string[]; constraints: string }) =>
    request<ComposeResponse>('/compose', { method: 'POST', body: JSON.stringify(payload) }),
  runOps: (payload: { workspace: string; input_text: string; constraints: string }) =>
    request<OpsResponse>('/ops/run', { method: 'POST', body: JSON.stringify(payload) })
};
