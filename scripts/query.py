#!/usr/bin/env python3
"""Run a SQL query against the built database and print the rows.

Usage: python scripts/query.py "SELECT id, title FROM sources"
Needs only the Python standard library; run scripts/build.py first.
"""

import sqlite3
import sys

from _load import ROOT

DB = ROOT / "build" / "self-facets.sqlite"


def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    if not DB.exists():
        print("No database yet. Run: python scripts/build.py")
        return 1
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = db.execute(sys.argv[1])
    if cur.description is None:
        return 0
    rows = [[("" if v is None else str(v)) for v in row] for row in cur.fetchall()]
    heads = [d[0] for d in cur.description]
    widths = [min(60, max(len(h), *(len(r[i]) for r in rows))) if rows else len(h) for i, h in enumerate(heads)]
    line = lambda cells: "  ".join(c[:w].ljust(w) for c, w in zip(cells, widths)).rstrip()
    print(line(heads))
    print(line(["-" * w for w in widths]))
    for row in rows:
        print(line(row))
    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
