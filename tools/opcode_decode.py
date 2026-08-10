#!/usr/bin/env python3
"""Work out how long each script opcode is, so the stream can be walked properly.

Anchor on text the corpus already trusts: every corpus line ends at an opcode,
so for each opcode we ask how many bytes must be skipped before Japanese resumes.

Scoring has to be strict. A naive "first distance that decodes as Japanese" wins
at +1 for two-byte opcodes, because the subcode byte itself decodes to some kana
and the genuine text right after it dilutes the score. So instead of taking the
first hit we score every distance and prefer the one whose run starts cleanly,
breaking ties toward the shorter skip.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(f"{OV}/ov28.bin", "rb").read()

JP = lambda c: ("぀" <= c <= "ヿ" or "一" <= c <= "鿿" or c in "。、！？・～「」（）ー")


def run_at(buf, i, limit=40):
    out = []
    while i < len(buf) and buf[i] < 0xF8 and len(out) < limit:
        cc, nxt = P.bytes_to_cc(buf, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        out.append(ch)
        i = nxt
    return "".join(out)


def score(s):
    """How much this looks like the start of authored dialogue."""
    if len(s) < 3:
        return 0.0
    head = sum(1 for c in s[:3] if JP(c)) / 3     # must START clean
    body = sum(1 for c in s if JP(c)) / len(s)
    return head * body


lines = []
for ln in open(f"{OV}/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        lines.append((int(p[0], 16), int(p[1]), p[3]))

best = collections.defaultdict(collections.Counter)
seen = collections.Counter()

for addr, ln, _ in lines:
    end = addr + ln
    if end + 12 >= len(ov):
        continue
    op = ov[end]
    if op < 0xF8:
        continue
    # F8 is a prefixed opcode: F8 <sub> [args]; others are bare.
    key = f"F8 {ov[end+1]:02X}" if op == 0xF8 else f"{op:02X}"
    lo = 2 if op == 0xF8 else 1
    seen[key] += 1
    cands = []
    for d in range(lo, 11):
        sc = score(run_at(ov, end + d))
        if sc >= 0.8:
            cands.append((d, sc))
    if cands:
        # shortest distance that scores well
        best[key][min(d for d, _ in cands)] += 1

print(f"{'opcode':>8} {'seen':>6} {'len':>4} {'conf':>6}   skip histogram")
for key, n in seen.most_common(30):
    h = best[key]
    if not h:
        print(f"{key:>8} {n:6d} {'?':>4} {'':>6}   (no clean resume)")
        continue
    d, c = h.most_common(1)[0]
    hist = " ".join(f"+{k}:{v}" for k, v in sorted(h.items()))
    print(f"{key:>8} {n:6d} {d:4d} {c/sum(h.values()):6.0%}   {hist}")
