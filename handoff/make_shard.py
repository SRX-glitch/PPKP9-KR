#!/usr/bin/env python3
"""Cut the worklist into shard files sized to be ONE request. Stdlib only.

    python make_shard.py            # 50 lines per shard, highest impact first
    python make_shard.py 50 12      # only the first 12 shards

**One shard = one AI request.** The default is 50 because that is the largest
chunk that holds quality; the first handoff round used 150-line shards, each fed
to a model in a single request, and accuracy fell off a cliff after roughly the
first hundred lines -- later shards came back with Korean that had nothing to do
with the Japanese on the same row. Do not raise this to "save round trips".

Shards come out of `data/untranslated.tsv` in its existing order, which is by
in-game occurrence count -- so shard_001 is the most-seen text in the game and
stopping early still leaves the player with the most visible half translated.
"""
import sys, os

# Paths printed here can contain Hangul; keep them readable when stdout is a
# pipe rather than a console (see the same note in validate.py).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "data", "untranslated.tsv")
DST = os.path.join(HERE, "work")

# The columns a translator needs in front of them, and nothing else.
COLS = ["id", "occ", "max", "prev", "jp", "next", "ko"]


def main(size=50, limit=None):
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().splitlines()
    head, body = lines[0].split("\t"), lines[1:]
    idx = [head.index(c) for c in COLS]

    os.makedirs(DST, exist_ok=True)
    made = 0
    for k in range(0, len(body), size):
        if limit is not None and made >= limit:
            break
        chunk = body[k:k + size]
        made += 1
        path = os.path.join(DST, f"shard_{made:03d}.tsv")
        if os.path.exists(path):
            print(f"skip {os.path.basename(path)} (already exists)")
            continue
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("\t".join(COLS) + "\n")
            for ln in chunk:
                p = ln.split("\t")
                f.write("\t".join(p[i] if i < len(p) else "" for i in idx) + "\n")
    print(f"{made} shard(s) of {size} lines in {DST}")
    if size > 50:
        print(f"WARNING: {size} lines per shard. Quality collapsed at 150 in the "
              f"first round -- keep one shard to one request, 50 lines or fewer.")
    print("Fill the `ko` column only, then: python validate.py work/shard_001.tsv")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 50,
         int(sys.argv[2]) if len(sys.argv) > 2 else None)
