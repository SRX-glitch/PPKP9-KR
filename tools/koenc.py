#!/usr/bin/env python3
"""Korean -> PokeTEXT byte encoder for PPKP9.

Charcode allocation lives in survey/font/kr_map.json:
  { "syl": {"응": 3519, ...},      # Hangul syllable -> charcode (2-byte)
    "one": {" ": 148, ...} }       # chars given a reclaimed 1-BYTE charcode

Everything else falls through to the game's own characters (。、？！「」 etc.
are already 1-byte, which is what makes short lines fit at all).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import poketbl as P

MAP = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/font/kr_map.json"


class Encoder:
    def __init__(self, mapping=None):
        m = mapping if mapping is not None else json.load(open(MAP, encoding="utf-8"))
        self.syl = {k: int(v) for k, v in m["syl"].items()}
        self.one = {k: int(v) for k, v in m.get("one", {}).items()}
        # Literal bytes that are NOT a charcode lookup. The Korean word space is
        # one: byte 0x00 draws a single 4px blank column (render_char's zero
        # path) where any real charcode costs a full 12px cell, and it needs no
        # glyph, so no Japanese character has to be sacrificed to host it.
        # charcode() deliberately returns None for these, which is what keeps
        # them out of MTE dictionary entries -- a 0 halfword terminates an entry.
        self.raw = {k: bytes.fromhex(v) for k, v in m.get("raw", {}).items()}
        # MTE dictionary: substring -> MTE charcode (expanded by the ARM9 hook)
        self.mte = {k: int(v) for k, v in m.get("mte", {}).items()}
        self._mte_sorted = sorted(self.mte, key=len, reverse=True)

    def charcode(self, ch):
        if ch in self.one:
            return self.one[ch]
        if ch in self.syl:
            return self.syl[ch]
        return P.CH2CC.get(ch)

    def encode(self, text):
        out = bytearray()
        i = 0
        while i < len(text):
            hit = None
            for sub in self._mte_sorted:
                if text.startswith(sub, i):
                    hit = sub
                    break
            if hit:
                out += P.cc_to_bytes(self.mte[hit])
                i += len(hit)
                continue
            ch = text[i]
            if ch in self.raw:
                out += self.raw[ch]
                i += 1
                continue
            cc = self.charcode(ch)
            if cc is None:
                raise KeyError(f"no charcode for {ch!r} in {text!r}")
            out += P.cc_to_bytes(cc)
            i += 1
        return bytes(out)

    def decode(self, data):
        """inverse, for verification"""
        rev = {v: k for k, v in self.syl.items()}
        rev.update({v: k for k, v in self.one.items()})
        rev.update({v: k for k, v in self.mte.items()})
        rawrev = {v: k for k, v in self.raw.items()}
        s = []
        i = 0
        while i < len(data):
            hit = next((b for b in rawrev if data[i:i + len(b)] == b), None)
            if hit is not None:
                s.append(rawrev[hit])
                i += len(hit)
                continue
            cc, i = P.bytes_to_cc(data, i)
            if cc is None:
                s.append("?")
                continue
            s.append(rev.get(cc) or P.CC2CH.get(cc, "?"))
        return "".join(s)


def needed_chars(texts):
    """characters that require a NEW charcode (not already in the game font)"""
    need = set()
    for t in texts:
        for ch in t:
            if ch not in P.CH2CC:
                need.add(ch)
    return need
