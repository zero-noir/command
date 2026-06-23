from fastapi import APIRouter
from pydantic import BaseModel, Field
from services.ai_client import AIClient
import json
from pathlib import Path

router=APIRouter()
DATA = Path(__file__).resolve().parents[1] / 'data' / 'agents.json'

class OpsRequest(BaseModel):
    workspace: str = Field(default='meeting')
    input_text: str = Field(min_length=5)
    constraints: str = ''

@router.get('/health')
def health():
    return {'ok': True, 'app':'startup_ops_workspace', 'ai_enabled': AIClient().enabled(), 'workspaces':['meeting','media','product','finance','strategy']}

@router.get('/agents')
def agents():
    return json.loads(DATA.read_text(encoding='utf-8'))

@router.post('/ops/run')
async def run_ops(req: OpsRequest):
    labels={
      'meeting':'Meeting summary and keynote extraction',
      'media':'Paid media plan and creative testing',
      'product':'Product iteration and experiment planning',
      'finance':'Cost, pricing and profit margin review',
      'strategy':'Strategic brief and operating plan'
    }
    fallback={
      'title': labels.get(req.workspace, 'Operating brief'),
      'summary': f'Processed the {req.workspace} input into a practical operating brief. Offline mode uses structured heuristics; AI mode will rewrite this with model reasoning.',
      'decisions':['Clarify the owner for the next decision','Reduce the workflow to one measurable operating question','Review the result after one execution cycle'],
      'actions':['Assign one accountable owner','Define a success metric before execution','Create a 7-day review checkpoint'],
      'risks':['Unclear ownership','Metrics not tied to profit or growth','Too many initiatives at once'],
      'metrics':['Cycle time','Completion rate','Margin/CAC movement','Decision quality'],
      'next_brief':'Use the output as the handoff memo for the next operating review.'
    }
    system='You are a startup chief of staff and operating analyst. Convert the user input into concise, practical JSON for a founder/operator. Return title, summary, decisions, actions, risks, metrics, next_brief.'
    user=f'Workspace: {req.workspace} - {labels.get(req.workspace)}\nConstraints: {req.constraints}\nInput: {req.input_text[:9000]}'
    return await AIClient().complete_json(system, user, fallback)
