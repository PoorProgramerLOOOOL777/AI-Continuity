
# Instalación de la skill en Claude Code

1. Descomprime `AI-Continuity.zip`.
2. Copia la carpeta `skills/ai-continuity` al directorio de skills de Claude Code de tu usuario o proyecto. En instalaciones actuales suele ser:
   - Proyecto: `.claude/skills/ai-continuity/`
   - Usuario: `~/.claude/skills/ai-continuity/`
3. Copia el resto del proyecto a la raíz del repositorio donde quieras usar el motor externo.
4. Crea `.env` desde `.env.example` y configura tu gateway.
5. Instala dependencias con `pip install -r requirements.txt`.
6. Ejecuta `python -m continuity.cli handoff --summary "Inicio del proyecto"`.

La skill es la guía de trabajo; el motor Python es un prototipo separado. La skill no instala por sí sola integraciones de terceros ni cambia automáticamente el proveedor interno de Claude Code.
