
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "memory"
HANDOFF = ROOT / "handoff"

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""

def create_handoff(summary: str = "") -> Path:
    HANDOFF.mkdir(exist_ok=True)
    sections = [
        "# AI Continuity — handoff",
        f"Fecha UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Resumen de la sesión",
        summary.strip() or "(Añade un resumen de lo que se estaba haciendo.)",
    ]
    for filename, title in [
        ("project_context.md", "Contexto del proyecto"),
        ("decisions.md", "Decisiones técnicas"),
        ("completed_tasks.md", "Tareas completadas"),
        ("pending_tasks.md", "Tareas pendientes"),
    ]:
        sections += ["", f"## {title}", read_file(MEMORY / filename) or "(Sin información)"]
    sections += [
        "",
        "## Instrucciones para el siguiente modelo",
        "- Lee todo este handoff antes de modificar archivos.",
        "- Comprueba el estado real del repositorio; no asumas que el resumen está actualizado.",
        "- No repitas tareas ya completadas.",
        "- Si falta información crítica, pregunta antes de hacer cambios destructivos.",
        "- Actualiza los archivos de memoria y genera un nuevo handoff al terminar.",
    ]
    path = HANDOFF / "latest_handoff.md"
    path.write_text("\n".join(sections) + "\n", encoding="utf-8")
    return path

def load_handoff() -> str:
    path = HANDOFF / "latest_handoff.md"
    if not path.exists():
        return "No existe handoff. Lee memory/project_context.md y crea uno antes de continuar."
    return path.read_text(encoding="utf-8")
