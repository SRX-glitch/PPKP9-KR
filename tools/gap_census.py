#!/usr/bin/env python3
"""How much authored dialogue does the corpus truncate?

For every line the corpus recorded, look at the opcode that stopped the scan and
at what immediately follows it. If the opcode is an *inline* control code (name
insert, colour change) then real dialogue continues past it and the corpus threw
that remainder away.

The scan in text_budget.py stops at the first byte >= 0xF8 (or a 0x00) and then
resumes recording only at the next F8 6B, so every such remainder is lost.
"""
import os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

BASE = r"C:/Users/jngji/Desktop/실험실"
OV = f"{BASE}/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"
ov = open(f"{OV}/ov28.bin", "rb").read()


def decode(buf, i, end):
    """Decode charcode bytes i..end; returns text (stops at anything unmapped)."""
    out = []
    while i < end:
        cc, nxt = P.bytes_to_cc(buf, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        out.append(ch)
        i = nxt
    return "".join(out)


def text_run(buf, i):
    """Longest clean charcode run starting at i -> (text, end_index)."""
    out = []
    while i < len(buf) and buf[i] < 0xF8:
        cc, nxt = P.bytes_to_cc(buf, i)
        ch = P.CC2CH.get(cc)
        if ch is None:
            break
        out.append(ch)
        i = nxt
    return "".join(out), i


lines = []
for ln in open(f"{OV}/dialogue_lines.tsv", encoding="utf-8").read().splitlines():
    p = ln.split("\t")
    if len(p) >= 4:
        lines.append((int(p[0], 16), int(p[1]), p[3]))

stop_op = collections.Counter()
resumes = collections.Counter()      # opcode -> how often real text follows it
extra_chars = collections.Counter()  # opcode -> total dropped characters
samples = {}

for addr, ln, text in lines:
    end = addr + ln
    if end + 1 >= len(ov):
        continue
    op = ov[end]
    key = f"{op:02X} {ov[end+1]:02X}" if op >= 0xF8 else f"{op:02X}(zero)"
    stop_op[key] += 1
    # does dialogue continue right after this 2-byte code?
    nxt, _ = text_run(ov, end + 2)
    # Filter bytecode that happens to decode as charcodes: demand a run that is
    # mostly kana/kanji/punctuation, the way authored dialogue actually reads.
    def jp_like(s):
        if len(s) < 3:
            return False
        good = sum(1 for c in s
                   if "぀" <= c <= "ヿ" or "一" <= c <= "鿿" or c in "。、！？・～「」（）")
        return good / len(s) >= 0.8
    if jp_like(nxt):
        resumes[key] += 1
        extra_chars[key] += len(nxt)
        samples.setdefault(key, (text, nxt, addr))

print(f"corpus lines examined: {len(lines)}\n")
print("opcode that stopped the scan -> (times, times real text follows, chars dropped)")
print(f"{'opcode':>12}  {'lines':>6}  {'continues':>9}  {'chars lost':>10}")
for key, n in stop_op.most_common(20):
    print(f"{key:>12}  {n:6d}  {resumes[key]:9d}  {extra_chars[key]:10d}")

tot_lines = sum(resumes.values())
tot_chars = sum(extra_chars.values())
print(f"\nlines whose remainder was dropped : {tot_lines} of {len(lines)}"
      f" ({tot_lines/len(lines):.1%})")
print(f"Japanese characters never extracted: {tot_chars}")

print("\nexamples (recorded  ||  dropped remainder):")
for key, n in resumes.most_common(8):
    rec, nxt, addr = samples[key]
    print(f"  [{key}] @{addr:#08x}\n      recorded: {rec}\n      dropped : {nxt}")
