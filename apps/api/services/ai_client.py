import json
import httpx
from core.config import settings

class AIClient:
    def enabled(self) -> bool:
        return (settings.llm_provider == "deepseek" and bool(settings.deepseek_api_key)) or (settings.llm_provider == "gemini" and bool(settings.gemini_api_key))

    async def complete_json(self, system: str, user: str, fallback: dict) -> dict:
        if not self.enabled():
            return {**fallback, "ai_mode": "offline_deterministic"}
        try:
            if settings.llm_provider == "deepseek":
                return await self._deepseek(system, user, fallback)
            if settings.llm_provider == "gemini":
                return await self._gemini(system, user, fallback)
        except Exception as exc:
            return {**fallback, "ai_mode": "fallback_after_error", "model_error": str(exc)[:240]}
        return {**fallback, "ai_mode": "offline_deterministic"}

    async def _deepseek(self, system: str, user: str, fallback: dict) -> dict:
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            r = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {settings.deepseek_api_key}", "Content-Type": "application/json"},
                json={
                    "model": settings.deepseek_model,
                    "messages": [{"role":"system","content": system}, {"role":"user","content": user}],
                    "temperature": 0.25,
                    "response_format": {"type": "json_object"},
                },
            )
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            return {**json.loads(content), "ai_mode": "deepseek", "model": settings.deepseek_model}

    async def _gemini(self, system: str, user: str, fallback: dict) -> dict:
        prompt = system + "\n\nReturn valid JSON only.\n\n" + user
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
        async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
            r = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.25, "responseMimeType": "application/json"}})
            r.raise_for_status()
            text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            return {**json.loads(text), "ai_mode": "gemini", "model": settings.gemini_model}
