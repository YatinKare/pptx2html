# examples/runner.py
from __future__ import annotations

import argparse
import pathlib

from pptx2html import parse_pptx  # your public API


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to .pptx")
    ap.add_argument("--out", default="out_user", help="Output directory")
    ap.add_argument("--debug", action="store_true", help="Return/report diagnostics")
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # run conversion
    report = parse_pptx(args.input, str(out), debug=args.debug)

    # print a simple, user-friendly summary
    print("✅ Conversion complete")
    print(f"   input : {pathlib.Path(args.input).resolve()}")
    print(f"   output: {out.resolve()}")

    # optional: show a terse debug summary
    if args.debug and report is not None:
        # keep this short; your reporting module can format rich details later
        print("\n[debug] issues:", getattr(report, "issue_count", "n/a"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
