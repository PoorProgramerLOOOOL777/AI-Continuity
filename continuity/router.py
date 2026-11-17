
import json
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

def load_models() -> dict[str, Any]:
    with (ROOT / "config" / "models.json").open(encoding="utf-8") as f:
        return json.load(f)

def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {429, 500, 502, 503, 504}
    if isinstance(exc, httpx.TimeoutException):
        return True
    message = str(exc).lower()
    return any(term in message for term in ("quota", "rate limit", "insufficient_quota", "overloaded"))

async def chat(prompt: str, system: str = "") -> str:
    base_url = os.getenv("AI_BASE_URL", "").rstrip("/")
    api_key = os.getenv("AI_API_KEY", "")
    timeout = float(os.getenv("AI_TIMEOUT", "90"))
    if not base_url or not api_key:
        raise RuntimeError("Configura AI_BASE_URL y AI_API_KEY en el archivo .env")

    config = load_models()
    models = [m for m in config.get("models", []) if m.get("enabled", True)]
    if not models:
        raise RuntimeError("No hay modelos habilitados en config/models.json")

    errors = []
    async with httpx.AsyncClient(timeout=timeout) as client:
        for model in models[:config.get("retry", {}).get("max_models", 4)]:
            payload = {
                "model": model["id"],
                "messages": ([{"role": "system", "content": system}] if system else [])
                           + [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            try:
                response = await client.post(
                    f"{base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as exc:
                errors.append(f'{model["id"]}: {type(exc).__name__}: {exc}')
                if not is_retryable(exc):
                    # Errores de autenticación/configuración no se arreglan cambiando de modelo.
                    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code in {400, 401, 403, 404}:
                        raise RuntimeError(errors[-1]) from exc
                continue

    raise RuntimeError("Ningún modelo pudo responder:\n" + "\n".join(errors))
