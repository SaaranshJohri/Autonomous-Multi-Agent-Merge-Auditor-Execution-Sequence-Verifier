
import argparse
import json
import sys
from pathlib import Path

from mergemind.engine import analyze_file, analyze_merge_files


def build_parser():
    parser = argparse.ArgumentParser(
        prog="mergemind",
        description="Semantic merge conflict analysis toolkit",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a Python source file",
    )
    analyze_parser.add_argument("file", help="Path to Python file")

    merge_parser = subparsers.add_parser(
        "merge",
        help="Analyze three versions of a Python file",
    )
    merge_parser.add_argument("--base", required=True, help="Base version")
    merge_parser.add_argument("--a", required=True, help="Developer A version")
    merge_parser.add_argument("--b", required=True, help="Developer B version")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "analyze":
            result = analyze_file(args.file)
        elif args.command == "merge":
            result = analyze_merge_files(
                args.base,
                args.a,
                args.b,
            )
        else:
            parser.error("Unknown command")
            return

        print(json.dumps(result, indent=2, default=str))

    except FileNotFoundError as exc:
        print(f"File error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except SyntaxError as exc:
        print(
            f"Python syntax error at line {exc.lineno}: {exc.msg}",
            file=sys.stderr,
        )
        raise SystemExit(1)
    except Exception as exc:
        print(f"MergeMind error: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
