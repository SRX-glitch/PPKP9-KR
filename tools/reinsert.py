#!/usr/bin/env python3
"""Text reinsertion: re-encode a replacement string and patch it into the ROM at a
given offset (pad with 0x00 if shorter; refuse if longer). Verifies by re-decoding.
Demonstrates the text-patch pipeline on the uncompressed ROM dialogue."""
import sys
sys.path.insert(0,".")
from importlib import import_module
pe=import_module("tools.pokeencode") if False else None
# inline import
import importlib.util, os
spec=importlib.util.spec_from_file_location("pe", os.path.join(os.path.dirname(__file__),"pokeencode.py"))
pe=importlib.util.module_from_spec(spec); spec.loader.exec_module(pe)

CS=sys.argv[1]; ROM=sys.argv[2]
T=pe.load_tables(CS); dec,enc=pe.build_maps(T)
rom=bytearray(open(ROM,"rb").read())

# demo: at a known dialogue offset, read original, replace with a new (same-encoding) line
DEMOS=[
    (0x55E18D, "よくわからないけど、やってみようか。", "テストせいこう！ほんやくOK。"),  # replace with new JP (proof)
]
for off,orig_expect,newtext in DEMOS:
    # decode original at offset
    orig=pe.decode(rom[off:off+80], T=T)
    ob,_=pe.encode(orig_expect,enc)
    nb,bad=pe.encode(newtext,enc)
    if nb is None:
        print(f"0x{off:X}: cannot encode replacement (char U+{ord(bad):04X})"); continue
    print(f"0x{off:X}: orig_decoded_len={len(orig)} orig_expect_bytes={len(ob)} new_bytes={len(nb)}")
    if len(nb)>len(ob):
        print("  replacement longer than original — would need pointer/relocation; skipping write"); continue
    # patch: write new bytes, pad remaining original span with 0x00
    span=len(ob)
    rom[off:off+span]=nb + b"\x00"*(span-len(nb))
    back=pe.decode(rom[off:off+span], T=T)
    print(f"  patched. re-decoded: matches new? {back.startswith(newtext.rstrip('。'))} -> [{back}]")
open("/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/rom_textpatch_demo.nds" if False else ROM+".patched","wb").write(rom)
print("wrote", ROM+".patched")
