#!/usr/bin/env python3
"""Assert that no byte the original used as an OPCODE moved in the patch.

This generalises the `F8 15` gate in build_kr. That defect -- the run walker
starting a text run on a choice list's count operand, so the redirect escape
overwrote it and the box drew nothing -- is a whole class: any opcode whose
declared width is short lets a run start inside it, and patching that run
corrupts the code.

The method is the one that found it: walk the ORIGINAL overlay with the same
opcode table the extractor uses, record every byte that belongs to an opcode
(lead + operands), and require the patched overlay to hold those bytes
unchanged. Text bytes are free to change; opcode bytes are not.

⚠ This is self-consistent, not absolute. The walk uses opcode_lengths.json, so an
opcode whose recorded width is still wrong is mis-parsed identically in both
passes and slips through -- exactly how `F8 15` hid. It catches *drift* between
what we parse and what we write, which is most of the risk, but a width error
found here needs a second witness (structure, or the screen).

    python tools/check_opcodes.py
    python tools/check_opcodes.py --rom OTHER.nds
"""
import argparse, collections, json, os, sys

BASE = r"C:/Users/jngji/Desktop/실험실"
ORIG = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
OV = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/ov28"


def overlay(rom):
    f = int.from_bytes(rom[0x48:0x4C], "little")
    lo = int.from_bytes(rom[f + 25 * 8:f + 25 * 8 + 4], "little")
    hi = int.from_bytes(rom[f + 25 * 8 + 4:f + 25 * 8 + 8], "little")
    return lo, hi


def opcode_bytes(ov, lo, hi, bare, f8):
    """Offsets (relative to lo) that belong to an opcode, not to text."""
    owned = bytearray(hi - lo)
    i = lo
    while i < hi - 2:
        b = ov[i]
        # Charcode-aware, and it has to be: lead bytes 0xE8-0xF7 take a second
        # byte that can be ANY value, 0xF8-0xFF included. Walking byte-by-byte
        # instead reads those second bytes as opcode leads and reports thousands
        # of "corrupted opcodes" that are really ordinary text -- `e8 fc` inside
        # 「君と一緒に過ごしました。）」 was one. Same contamination that hid the real
        # F8 15 defect; do not simplify this away.
        if 0xE8 <= b <= 0xF7:
            i += 2
            continue
        if b == 0 or b < 0xE8:
            i += 1
            continue
        # F9 is a fixed 2-byte opcode (reanalysis handler proof) -- it does NOT
        # take an F8-style subcode, so it must go through `bare` (249: 2), not
        # the f8 width table.
        if b == 0xF8:
            n = f8.get(ov[i + 1], 2)
        else:
            n = bare.get(b, 1)
        for k in range(min(n, hi - i)):
            owned[i - lo + k] = 1
        i += n
    return owned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds")
    a = ap.parse_args()

    orig = open(ORIG, "rb").read()
    new = open(a.rom, "rb").read()
    olo, ohi = overlay(orig)
    nlo, _ = overlay(new)
    shift = nlo - olo

    L = json.load(open(os.path.join(OV, "opcode_lengths.json"), encoding="utf-8"))
    bare = {int(k): v for k, v in L["bare"].items()}
    f8 = {int(k): v for k, v in L["f8"].items()}

    owned = opcode_bytes(orig, olo, ohi, bare, f8)
    diff = collections.Counter()
    examples = []
    for k in range(ohi - olo):
        if owned[k] and orig[olo + k] != new[nlo + k + 0]:
            lead = None
            for back in range(0, 9):
                if k - back >= 0 and orig[olo + k - back] >= 0xF8:
                    lead = (orig[olo + k - back], back)
                    break
            diff[lead] += 1
            if len(examples) < 12:
                examples.append((olo + k, orig[olo + k], new[nlo + k]))
    total = sum(owned)
    print(f"오버레이 {ohi - olo:,}B 중 옵코드 바이트 {total:,}개")
    print(f"패치본에서 바뀐 옵코드 바이트: {sum(diff.values()):,}개")
    if diff:
        print("\n리드별 (리드바이트, 리드로부터의 거리):")
        for k, v in diff.most_common(12):
            print(f"   {k}  {v}개")
        print("\n예:")
        for off, o, n in examples:
            print(f"   ROM {off:#x}  {o:#04x} -> {n:#04x}")
    sys.exit(1 if diff else 0)


if __name__ == "__main__":
    main()
