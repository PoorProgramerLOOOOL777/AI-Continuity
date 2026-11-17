
import argparse
import asyncio
from pathlib import Path

from .handoff import create_handoff, load_handoff
from .router import chat

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(prog="continuity", description="AI Continuity")
    sub = parser.add_subparsers(dest="command", required=True)

    hp = sub.add_parser("handoff", help="Crear/actualizar el resumen de transferencia")
    hp.add_argument("--summary", default="")

    sub.add_parser("show", help="Mostrar el último handoff")

    cp = sub.add_parser("chat", help="Enviar una petición y probar modelos en orden")
    cp.add_argument("--prompt", required=True)

    args = parser.parse_args()
    if args.command == "handoff":
        print(f"Handoff creado: {create_handoff(args.summary)}")
    elif args.command == "show":
        print(load_handoff())
    elif args.command == "chat":
        context = load_handoff()
        print(asyncio.run(chat(args.prompt, system=(
            "Eres el modelo de continuidad de un proyecto. Lee el handoff, conserva las decisiones "
            "y continúa desde el punto pendiente. Si el handoff no contiene datos suficientes, dilo.\n\n"
            + context
        ))))

if __name__ == "__main__":
    main()
