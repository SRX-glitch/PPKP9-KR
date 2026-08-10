#!/usr/bin/env python3
"""Report run/char coverage of the current translation set against the corpus."""
import os, sys, glob, collections

BASE = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"


def done_set():
    done = set()
    names = ["common_lines"] + sorted(
        (os.path.splitext(os.path.basename(p))[0]
         for p in glob.glob(f"{BASE}/translation/batch*.tsv")),
        key=lambda n: int(n[5:]))
    for name in names:
        p = f"{BASE}/translation/{name}.tsv"
        if not os.path.exists(p):
            continue
        for ln in open(p, encoding="utf-8").read().splitlines()[1:]:
            if "\t" in ln:
                jp, ko = ln.split("\t")[0].strip(), ln.split("\t")[1].strip()
                if jp and ko:
                    done.add(jp)
    return done


def main():
    done = done_set()
    runs = []
    for ln in open(f"{BASE}/survey/ov28/dialogue_runs.tsv", encoding="utf-8").read().splitlines():
        p = ln.split("\t")
        if len(p) >= 4:
            runs.append(p[3])
    occ = collections.Counter(runs)
    hit = sum(n for jp, n in occ.items() if jp in done)
    chars = sum(n * len(jp) for jp, n in occ.items())
    hitc = sum(n * len(jp) for jp, n in occ.items() if jp in done)
    dh = sum(1 for jp in occ if jp in done)
    print(f"translated entries : {len(done)}")
    print(f"runs      : {hit}/{len(runs)} = {100*hit/len(runs):.2f}%")
    print(f"chars     : {hitc}/{chars} = {100*hitc/chars:.2f}%")
    print(f"distinct  : {dh}/{len(occ)} = {100*dh/len(occ):.2f}%")
    print(f"5% of runs = {round(0.05*len(runs))} occurrences")


if __name__ == "__main__":
    main()
