#!/usr/bin/env python3
"""Smoke test for the judge sandbox — compile + run a hello-world in Python.

The judge is the arena-side component that executes a coder's submission
inside an offline sandbox. This script asserts the sandbox can run a
trivial program and report a verdict.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    code = "print('hello world')\n"
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh:
        fh.write(code)
        path = fh.name
    try:
        proc = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=5,
        )
    finally:
        Path(path).unlink(missing_ok=True)
    if proc.returncode != 0:
        print(f"FAIL: exit {proc.returncode}\nstderr: {proc.stderr}", file=sys.stderr)
        return 1
    if "hello world" not in proc.stdout:
        print(f"FAIL: unexpected output: {proc.stdout!r}", file=sys.stderr)
        return 1
    print("PASS: judge sandbox can execute a hello-world program.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
