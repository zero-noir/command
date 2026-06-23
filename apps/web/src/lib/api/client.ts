const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) }, ...init });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<T>;
}
export type Agent = { id:string; title:string; domain:string; path:string; excerpt:string; source:string; capability_tags:string[]; good_for:string[] };
export type ComposeResponse = { objective:string; ai_mode:string; selected_agents: Agent[]; workflow_steps:{title:string; owner:string; action:string; output:string}[]; operating_risks:string[]; success_metrics:string[]; handoff_brief:string };
export type OpsResponse = { ai_mode:string; title:string; summary:string; decisions:string[]; actions:string[]; risks:string[]; metrics:string[]; next_brief:string };
export const api = {
  health: () => request<any>('/api/health'),
  agents: () => request<Agent[]>('/api/agents'),
  compose: (payload: {objective:string; agent_ids:string[]; constraints:string}) => request<ComposeResponse>('/api/compose', { method:'POST', body: JSON.stringify(payload) }),
  runOps: (payload: {workspace:string; input_text:string; constraints:string}) => request<OpsResponse>('/api/ops/run', { method:'POST', body: JSON.stringify(payload) })
};
