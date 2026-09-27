#!/usr/bin/env python3
"""Shared PokeTEXT character tables + charcode mapping."""
import re, os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
# Character tables live in the repo as JSON (survey/common/poketext_tables.json).
# The decompiled PokeTEXT source they were derived from is third-party code and is
# NOT tracked; it is only consulted to regenerate the JSON when present.
TBL_JSON = os.path.join(_HERE, "..", "survey", "common", "poketext_tables.json")
CS = os.path.join(_HERE, "..", "poketext_src", "PokeTEXT.decompiled.cs")


def _load():
    if os.path.exists(TBL_JSON) and not os.environ.get("PPKP9_TABLES_FROM_CS"):
        d = json.load(open(TBL_JSON, encoding="utf-8"))
        return {int(k): v for k, v in d.items()}
    lines = open(CS, encoding="utf-8").read().splitlines()
    in_poke3 = False
    tables = {}

    def unesc(s):
        return re.sub(r'\\u([0-9a-fA-F]{4})', lambda x: chr(int(x.group(1), 16)), s)

    for ln in lines:
        if "ポケ3以降の文字コード変換処理" in ln:
            in_poke3 = True
        m = re.search(r'array4\[(\d+)\]\s*=\s*"(.*)";\s*$', ln)
        if m and in_poke3:
            tables.setdefault(int(m.group(1)), []).append(unesc(m.group(2)))
    # Variant choice verified against the real ROM font in tools/pick_variants.py:
    # every table is JIS-ordered (table 2 = 亜唖娃阿…, continuing into tables 3-14).
    VARIANT = {1: 1, 2: 2}
    T = {}
    for i in range(1, 18):
        vv = tables.get(i, [])
        if not vv:
            T[i] = ""
            continue
        T[i] = vv[VARIANT.get(i, 0)] if VARIANT.get(i, 0) < len(vv) else vv[0]
    return T


T = _load()

# charcode -> character
CC2CH = {}
for i, ch in enumerate(T[1]):
    CC2CH[i] = ch                      # charcode 0..230
for t in range(2, 18):
    for j, ch in enumerate(T[t]):
        CC2CH[256 + (t - 2) * 256 + j] = ch
CH2CC = {}
for cc, ch in CC2CH.items():
    CH2CC.setdefault(ch, cc)


def cc_to_bytes(cc):
    """charcode -> PokeTEXT byte sequence."""
    if cc < 231:
        return bytes([cc + 1])
    t = (cc - 256) // 256          # 0..15  -> table 2..17
    j = (cc - 256) % 256
    return bytes([232 + t, j])


def bytes_to_cc(buf, i):
    b = buf[i]
    if 1 <= b <= 231:
        return b - 1, i + 1
    if 232 <= b <= 247:
        return 256 + (b - 232) * 256 + buf[i + 1], i + 2
    return None, i + 1


if __name__ == "__main__":
    print("table sizes:", {i: len(T[i]) for i in sorted(T)})
    print("charcodes mapped:", len(CC2CH))
    for cc in (0, 1, 2, 230, 256, 257):
        print(f"  cc {cc:4d} = {CC2CH.get(cc)!r}  bytes {cc_to_bytes(cc).hex()}")
