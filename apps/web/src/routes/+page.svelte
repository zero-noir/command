<script lang="ts">
  import { api, type OpsResponse } from '$lib/api/client';
  const workspaces = [
    { id:'meeting', label:'Meeting', hint:'decisions, action items, keynote points' },
    { id:'media', label:'Media', hint:'budget, tracking, creative tests' },
    { id:'product', label:'Product', hint:'feedback, experiments, iteration' },
    { id:'finance', label:'Finance', hint:'cost, pricing, margins' },
    { id:'strategy', label:'Strategy', hint:'briefs, tradeoffs, operating cadence' }
  ];
  let workspace = $state('meeting');
  let input_text = $state('We reviewed launch progress. Paid social has traffic but weak activation. Product onboarding is too long. Finance wants a clearer margin model before increasing spend. Team needs a tighter weekly cadence.');
  let constraints = $state('Keep outputs concise and action-oriented for a founder/operator.');
  let result = $state<OpsResponse | null>(null);
  let loading = $state(false);
  let error = $state('');
  let health = $state<any>(null);

  async function run() {
    loading = true;
    error = '';
    try {
      result = await api.runOps({ workspace, input_text, constraints });
    } catch (e) {
      error = e instanceof Error ? e.message : 'Run failed';
    } finally {
      loading = false;
    }
  }

  $effect(() => {
    api.health().then((h) => health = h).catch(() => {});
  });
</script>

<svelte:head><title>Startup Ops Workspace</title></svelte:head>

<main class="page">
  <aside class="sidebar">
    <div class="brand"><svg viewBox="0 0 40 40"><rect x="6" y="7" width="28" height="26" rx="8"/><path d="M14 22h12M14 16h8M14 28h6"/></svg><span>OpsRoom</span></div>
    <div class="status"><span class:online={health?.ai_enabled}></span>{health?.ai_enabled ? 'AI model connected' : 'Offline mode'}</div>
    <div class="menu">{#each workspaces as item}<button class:active={workspace===item.id} onclick={()=>workspace=item.id}><strong>{item.label}</strong><small>{item.hint}</small></button>{/each}</div>
  </aside>

  <section class="canvas">
    <header class="hero">
      <p>Founder operating workspace</p>
      <h1>Turn messy startup inputs into clean decisions, actions and metrics.</h1>
    </header>

    <section class="workbench">
      <div class="input-card">
        <div class="card-title"><h2>{workspaces.find(w=>w.id===workspace)?.label} input</h2><button onclick={run} disabled={loading}>{loading?'Running…':'Run workspace'}</button></div>
        <label for="source-input">Source notes, transcript, channel data or product feedback</label>
        <textarea id="source-input" bind:value={input_text}></textarea>
        <label for="constraints-input">Operating constraints</label>
        <input id="constraints-input" bind:value={constraints}/>
        {#if error}<p class="error">{error}</p>{/if}
      </div>

      <div class="output-card">
        {#if result}
          <div class="result-head"><span>{result.ai_mode}</span><h2>{result.title}</h2><p>{result.summary}</p></div>
          <div class="columns">
            <section><h3>Decisions</h3>{#each result.decisions as x}<p>{x}</p>{/each}</section>
            <section><h3>Actions</h3>{#each result.actions as x}<p>{x}</p>{/each}</section>
          </div>
          <div class="columns">
            <section><h3>Risks</h3>{#each result.risks as x}<p>{x}</p>{/each}</section>
            <section><h3>Metrics</h3>{#each result.metrics as x}<p>{x}</p>{/each}</section>
          </div>
          <div class="brief"><h3>Next brief</h3><p>{result.next_brief}</p></div>
        {:else}
          <div class="placeholder">
  <svg viewBox="0 0 640 420" aria-hidden="true" class="workspace-illustration">
    <defs>
      <linearGradient id="panelFill" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#fffdf8" />
        <stop offset="100%" stop-color="#f3eadb" />
      </linearGradient>
      <linearGradient id="accentLine" x1="0" x2="1">
        <stop offset="0%" stop-color="#b99b74" />
        <stop offset="100%" stop-color="#1b1a17" />
      </linearGradient>
    </defs>

    <rect x="96" y="64" width="448" height="292" rx="32" fill="url(#panelFill)" stroke="#e5d8c5" />
    <rect x="132" y="104" width="150" height="24" rx="12" fill="#1b1a17" opacity="0.9" />
    <rect x="132" y="144" width="250" height="12" rx="6" fill="#d9c8b0" />
    <rect x="132" y="168" width="198" height="12" rx="6" fill="#e4d7c5" />
    <rect x="132" y="192" width="226" height="12" rx="6" fill="#e4d7c5" />

    <rect x="132" y="248" width="108" height="54" rx="18" fill="#fffaf0" stroke="#dfcfba" />
    <rect x="266" y="248" width="108" height="54" rx="18" fill="#fffaf0" stroke="#dfcfba" />
    <rect x="400" y="248" width="108" height="54" rx="18" fill="#fffaf0" stroke="#dfcfba" />

    <path d="M240 275 H266" stroke="#b99b74" stroke-width="3" stroke-linecap="round" />
    <path d="M374 275 H400" stroke="#b99b74" stroke-width="3" stroke-linecap="round" />

    <circle cx="186" cy="275" r="7" fill="#1b1a17" />
    <circle cx="320" cy="275" r="7" fill="#1b1a17" />
    <circle cx="454" cy="275" r="7" fill="#1b1a17" />

    <path d="M420 122 C455 118 482 140 488 173 C493 202 476 230 448 240" fill="none" stroke="url(#accentLine)" stroke-width="4" stroke-linecap="round" />
    <path d="M438 109 L419 122 L438 135" fill="none" stroke="#1b1a17" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />

    <rect x="402" y="154" width="58" height="42" rx="14" fill="#fffdf8" stroke="#1b1a17" stroke-width="2" />
    <path d="M417 176 H445" stroke="#b99b74" stroke-width="3" stroke-linecap="round" />
  </svg>

  <p>Choose a workspace, paste rough notes, then produce an operator-ready output.</p>
</div>
        {/if}
      </div>
    </section>
  </section>
</main>

<style>
  :global(body){margin:0;background:#f7f3ea;color:#1b1a17;font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;font-size:14px}.page{min-height:100vh;display:grid;grid-template-columns:260px 1fr}.sidebar{background:#fffaf0;border-right:1px solid #e8dfcf;padding:22px 18px;display:flex;flex-direction:column;gap:22px}.brand{display:flex;align-items:center;gap:10px;font-weight:680;letter-spacing:-.03em}.brand svg{width:32px;height:32px}.brand rect{fill:#1b1a17}.brand path{stroke:#fffaf0;stroke-width:2;fill:none;stroke-linecap:round}.status{display:flex;align-items:center;gap:8px;border:1px solid #e7decd;background:#fffdf8;border-radius:999px;padding:8px 10px;color:#6f6659;font-size:12px}.status span{width:7px;height:7px;border-radius:50%;background:#b9afa0}.status span.online{background:#2e8c57}.menu{display:grid;gap:7px}.menu button{text-align:left;border:0;background:transparent;border-radius:14px;padding:11px;cursor:pointer;color:#5f584e}.menu button.active{background:#1b1a17;color:white}.menu strong{display:block;font-size:13px}.menu small{font-size:11px;opacity:.72}.canvas{padding:28px}.hero{max-width:780px;margin-bottom:24px}.hero p{text-transform:uppercase;letter-spacing:.14em;color:#937246;font-size:11px;margin:0 0 9px}.hero h1{font-size:30px;line-height:1.08;letter-spacing:-.045em;margin:0;font-weight:660}.workbench{display:grid;grid-template-columns:minmax(380px,.85fr) minmax(0,1.15fr);gap:16px}.input-card,.output-card{background:#fffdf8;border:1px solid #e9dfce;border-radius:24px;padding:18px;box-shadow:0 20px 60px rgba(66,49,26,.045)}.card-title{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:14px}h2{font-size:17px;margin:0;letter-spacing:-.02em}button{border:0;background:#1b1a17;color:white;border-radius:999px;padding:10px 14px;font-size:13px;cursor:pointer}button:disabled{opacity:.5}label{font-size:12px;color:#766e62;display:block;margin:12px 0 7px}textarea,input{width:100%;box-sizing:border-box;border:1px solid #e5dac7;background:white;border-radius:14px;padding:11px 12px;font:inherit;outline:none}textarea{min-height:360px;resize:vertical;line-height:1.5}.result-head span{display:inline-flex;border:1px solid #ded3bf;border-radius:999px;padding:5px 8px;font-size:11px;color:#7a6848}.result-head h2{font-size:22px;margin:12px 0 8px}.result-head p,.brief p{font-size:13px;color:#625b51;line-height:1.55}.columns{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}.columns section,.brief{border:1px solid #eee3d1;background:#fffaf0;border-radius:18px;padding:14px}.columns h3,.brief h3{margin:0 0 9px;font-size:13px}.columns p{margin:0 0 8px;font-size:12px;color:#625b51;line-height:1.45}.placeholder{display:grid;place-items:center;min-height:520px;color:#766e62;text-align:center;font-size:13px}.placeholder .workspace-illustration{
  width:min(560px,100%);
  max-height:380px;
}.error{font-size:12px;color:#9d3b2f}@media(max-width:1050px){.page{grid-template-columns:1fr}.sidebar{position:static}.workbench{grid-template-columns:1fr}.columns{grid-template-columns:1fr}}
</style>