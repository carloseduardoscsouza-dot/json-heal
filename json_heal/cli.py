"""
CLI interface for json-heal.
"""

import sys
import json
import argparse
from pathlib import Path
from . import __version__
from .healer import repair_json


def main():
    parser = argparse.ArgumentParser(
        prog="json-heal",
        description="Blazing-fast, zero-dependency JSON healer for LLM outputs.",
    )
    parser.add_argument("input", nargs="?", help="Broken JSON text to heal")
    parser.add_argument("-f", "--file", help="Path to file containing broken JSON")
    parser.add_argument("-o", "--output", help="Save healed JSON to file")
    parser.add_argument("-p", "--pretty", action="store_true", help="Pretty print healed JSON")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    content = ""
    if args.file:
        fpath = Path(args.file)
        if not fpath.exists():
            print(f"Error: File '{fpath}' not found.", file=sys.stderr)
            sys.exit(1)
        content = fpath.read_text(encoding="utf-8", errors="replace")
    elif args.input:
        content = args.input
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(0)

    fixed = repair_json(content)

    if args.pretty:
        try:
            parsed = json.loads(fixed)
            fixed = json.dumps(parsed, indent=2)
        except Exception:
            pass

    if args.output:
        Path(args.output).write_text(fixed, encoding="utf-8")
        print(f"Healed JSON written to: {args.output}")
    else:
        print(fixed)


if __name__ == "__main__":
    main()
