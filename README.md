
# AI Continuity

Un prototipo extensible para conservar el contexto de un proyecto y continuar el trabajo con otro modelo cuando un proveedor devuelve un error de cuota o límite.

## Qué incluye

- Skill de Claude Code en `skills/ai-continuity/SKILL.md`.
- CLI Python para crear y leer handoffs.
- Enrutador básico para APIs compatibles con OpenAI (por ejemplo, un gateway como OmniRoute si expone ese formato).
- Lista ordenada de modelos/proveedores configurable.
- Archivos persistentes de contexto, tareas y decisiones.
- Instrucciones para integrar Superpowers, I Have ADHD, Caveman y Headroom sin asumir que sus APIs o nombres de comandos son iguales.

## Importante: límites reales

Una skill de Claude no puede interceptar por sí sola el límite interno de Claude ni obligar a Claude Desktop/Claude Code a continuar en otra cuenta. Este proyecto ofrece dos mecanismos:

1. **Handoff manual o asistido:** Claude escribe el estado del proyecto en los archivos de memoria y el siguiente modelo lo lee.
2. **Enrutamiento externo:** el comando `continuity chat` envía una petición a un endpoint compatible con OpenAI y prueba el siguiente modelo si recibe un error de cuota/rate limit.

Para una conmutación automática dentro de Claude Code hace falta ejecutar el trabajo a través de un supervisor/gateway compatible o configurar un hook/launcher específico. No se debe prometer continuidad perfecta: el modelo nuevo reconstruye el contexto a partir del handoff, no recibe el estado interno privado del modelo anterior.

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`
- Una URL base de API compatible con OpenAI y una clave válida del gateway/proveedor.

## Inicio rápido

1. Descomprime el proyecto.
2. Copia `.env.example` a `.env` y configura `AI_BASE_URL` y `AI_API_KEY`.
3. Edita `config/models.json` y coloca primero los modelos que prefieres.
4. Instala dependencias: `pip install -r requirements.txt`.
5. Crea un handoff:
   `python -m continuity.cli handoff --summary "Estoy construyendo mi aplicación"`.
6. Envía una prueba:
   `python -m continuity.cli chat --prompt "Resume el estado del proyecto y dime el siguiente paso"`.

## Configuración de modelos

`config/models.json` admite una lista de modelos. Añade los identificadores que realmente exponga tu gateway. La cifra de modelos disponibles depende del proveedor, región, cuenta y configuración; el proyecto no garantiza que todos los modelos anunciados estén habilitados para tu clave.

## Integraciones

- **OmniRoute:** configura su URL base y los IDs de modelo que publique tu instancia. Si ofrece API compatible con OpenAI, el adaptador puede utilizarla.
- **Superpowers:** úsalo como metodología/herramientas de planificación y desarrollo; AI Continuity conserva sus planes y resultados en el handoff.
- **I Have ADHD:** integración conceptual opcional para dividir tareas en pasos pequeños. Añade sus instrucciones reales a la skill si tienes el paquete exacto.
- **Caveman:** integración conceptual opcional para respuestas concisas. No se presupone un endpoint o comando.
- **Headroom:** integración conceptual opcional para compresión de contexto. No se presupone un endpoint o comando.

Los nombres de skills/plugins pueden corresponder a proyectos distintos. Revisa sus instrucciones oficiales antes de automatizar comandos o permisos.

## Seguridad

- Nunca guardes claves API en `models.json`, `SKILL.md` ni en el repositorio.
- Usa `.env` local y no lo subas a GitHub.
- Revisa los comandos y cambios que genere cualquier modelo antes de ejecutarlos.
- No compartas archivos `.env`, tokens, claves SSH ni credenciales en los handoffs.
