#!/usr/bin/env python3
"""Rewrite hardcoded project paths after moving the work products into
Desktop/실험실/파워프로군 포켓9/.

Byte-level replacement on purpose: some sources are cp949 and some utf-8, and
decoding them just to substitute a path risks re-encoding damage elsewhere in
the file.  Anchoring on "실험실<sep><child>" is unambiguous, and the replacement
text already contains the new folder, so re-running is a no-op.

Usage:
    python3 _repath.py <root> [--apply]
"""
import sys, os

CHILDREN = ["ppkp9-kr", "rom", "_translation_backup_0235", "_translation_backup_review_1628"]
NEWDIR = "파워프로군 포켓9"
ENCODINGS = ["utf-8", "cp949"]
SEPS = ["/", "\\", "\\\\"]
EXTS = {".py", ".sh", ".json", ".md", ".txt", ".bat", ".cmd", ".cfg", ".ini", ".toml"}
MAXSIZE = 8 * 1024 * 1024


def rules():
    out = []
    for enc in ENCODINGS:
        for sep in SEPS:
            for child in CHILDREN:
                old = f"실험실{sep}{child}"
                new = f"실험실{sep}{NEWDIR}{sep}{child}"
                try:
                    out.append((old.encode(enc), new.encode(enc)))
                except UnicodeEncodeError:
                    pass
    # longest first so "\\\\" is tried before "\\"
    return sorted(set(out), key=lambda r: -len(r[0]))


def main():
    root = sys.argv[1]
    apply = "--apply" in sys.argv
    R = rules()
    total_files = total_hits = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() not in EXTS:
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > MAXSIZE:
                    continue
                data = open(p, "rb").read()
            except OSError:
                continue
            hits = 0
            out = data
            for old, new in R:
                c = out.count(old)
                if c:
                    out = out.replace(old, new)
                    hits += c
            if hits:
                total_files += 1
                total_hits += hits
                print(f"{'FIX ' if apply else 'would'} {hits:>3}  {os.path.relpath(p, root)}")
                if apply:
                    open(p, "wb").write(out)
    print(f"\n{total_files} file(s), {total_hits} occurrence(s)"
          f"{' rewritten' if apply else ' would change'}")


if __name__ == "__main__":
    main()
