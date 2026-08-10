#!/usr/bin/env python3
"""One bisection step: hold back some lines, rebuild to the TEST rom, play it.

Session 27 narrowed a blank-choice-screen regression to 21 lines held in
`translation/_marker_quarantine/015_markers.tsv` but ran out of budget before
naming the culprit. Each step used to be: edit a pending file, re-finalize,
build, then thirty-odd emulator calls. This does all of it from one command.

    python3 tools/bisect_lines.py --hold 0:11        # hold back the first 11 suspects
    python3 tools/bisect_lines.py --hold 11:21       # ... and the other half
    python3 tools/bisect_lines.py --hold none        # control: everything in

It never touches the deploy ROM -- output always goes to PPKP9_test.nds.
Run from WSL so the playtest step can reach the emulator binary.
"""
import argparse, os, shutil, subprocess, sys

# Two halves, two worlds. tl.py and build_kr.py hardcode Windows paths (poketbl
# reads C:/.../PokeTEXT.decompiled.cs), so the build must run on Windows Python.
# playtest.py drives the Linux-side emucap binary and `launch` only accepts
# /mnt/c paths, so it must run under WSL. Running the whole script under WSL
# fails at the first import -- and only AFTER batch120.tsv has been deleted.
WIN = os.name == "nt"
BASE = ("C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr" if WIN
        else "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr")
TEST_ROM = "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_test.nds"   # WSL form
SUSPECTS = f"{BASE}/translation/_marker_quarantine/015_markers.tsv"
PENDING15 = f"{BASE}/translation/pending/015.tsv"
# The verified-good 366 rows, frozen. Every run rebuilds pending/015 from THIS,
# never from whatever the previous run left behind -- otherwise a suspect added
# in round 1 is already in the file in round 2 and "holding it back" silently
# does nothing, which would make the whole bisection lie.
BASELINE = f"{BASE}/translation/_marker_quarantine/015_baseline.tsv"
# The 7 rows that are genuinely menu markers; proven NOT to be the cause on
# their own (holding back only these still reproduced the defect).
MARKERS = {"ははカーブ", "ひひフォーク", "ふふシンカー", "へへシュート",
           "いＯＫだ。", "い再挑戦だ！", "いまあ、やってみるか。"}


def rows(path):
    return [l for l in open(path, encoding="utf-8").read().splitlines()[1:] if "\t" in l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-play", action="store_true",
                    help="build only; skip the boot test")
    ap.add_argument("--hold", required=True,
                    help="'none' | 'ctrl' | 'misaligned' | a slice, e.g. 0:11")
    ap.add_argument("--tag", default="bis")
    a = ap.parse_args()

    suspects = [r for r in rows(SUSPECTS) if r.split("\t")[0] not in MARKERS]
    if a.hold == "none":
        held = []
    elif a.hold == "ctrl":
        # The six suspects that sit immediately after a control byte (>=0xF8)
        # in the ORIGINAL rom. PP7's report (rom/분석보고서/) found that kana
        # right after a tag are engine PARAMETERS, not display text, and that
        # translating them corrupts everything after.
        # Session 29 proved the parallel holds here: four pitch-name records sit
        # back to back in the same frame, and the only split that yields four
        # real words (カーブ/フォーク/シンカー/シュート) is `F8 <a> <b>` -- so F8
        # is three bytes, and FA/FB take operands too. An earlier note here
        # claimed PPKP9's FA/FB take none; that was wrong.
        want = {"いい？", "うーーーーーーん？", "ふふふふふふふふふっ・・・・",
                "いや、そんなつもりじゃ・・・", "いつまででも、この町に",
                "いいなぁ～って・・・"}
        held = [s for s in suspects if s.split("	")[0] in want]
    elif a.hold == "misaligned":
        # Everything tools/check_alignment.py flags, plus the two rows whose
        # lead is 0xFA. FA is excluded from the checker's width table on purpose
        # (its byte histogram is flat, so treating it as a code would fire on
        # ordinary text), but these two were confirmed by hand, so hold them
        # here rather than loosening the checker for every future worklist.
        import check_alignment as CA
        rom = open(CA.ORIG, "rb").read()
        want = {jp for jp, _, _ in CA.check(rom, SUSPECTS)}
        want |= {"いつまででも、この町に", "いいなぁ～って・・・", "いい？"}
        held = [s for s in suspects if s.split("\t")[0] in want]
    else:
        lo, _, hi = a.hold.partition(":")
        held = suspects[int(lo or 0):int(hi or len(suspects))]
    held_jp = {h.split("\t")[0] for h in held}

    # Rebuild pending/015 = the verified-good 366 rows + every suspect we are
    # NOT holding back this round + the 7 markers (never re-added; they are
    # innocent but out of scope for this hunt).
    keep = rows(BASELINE)
    keep_jp = {k.split("\t")[0] for k in keep}
    for s in suspects:
        if s.split("\t")[0] not in held_jp and s.split("\t")[0] not in keep_jp:
            keep.append(s)
    with open(PENDING15, "w", encoding="utf-8") as f:
        f.write("jp\tko\n" + "\n".join(keep) + "\n")
    print(f"holding back {len(held)} of {len(suspects)} suspects; "
          f"pending/015.tsv = {len(keep)} rows", flush=True)
    for h in held:
        print("   HELD", h)

    for p in (f"{BASE}/translation/batch120.tsv",):
        if os.path.exists(p):
            os.remove(p)
    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               PPKP9_ROMOUT="C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_test.nds")
    subprocess.run([sys.executable, "tools/tl.py", "finalize", "--batch", "120"],
                   cwd=BASE, env=env, check=True)
    # encoding must be explicit: on this Korean-locale box the parent decodes a
    # captured child as cp949 and dies on the first Hangul byte -- AFTER the ROM
    # has already been written, so the run looks like a build failure when the
    # build actually succeeded.
    r = subprocess.run([sys.executable, "tools/build_kr.py"], cwd=BASE, env=env,
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    for line in r.stdout.splitlines():
        if "verify" in line or "grows" in line:
            print("  " + line, flush=True)
    if r.returncode:
        sys.exit("build failed:\n" + r.stdout[-2000:])

    if a.no_play:
        print("built; --no-play, so not booting it")
        return
    # 0.02 was too tight: presses landed mid-transition and were dropped.
    # 0.3 is what the runs that finally got through creation used.
    play = ("python3 tools/playtest.py --rom '%s' --scene choice --tag %s --gap 0.3"
            % (TEST_ROM, a.tag))
    if WIN:
        cd = "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr"
        subprocess.run(["wsl", "-e", "bash", "-lc", f"cd {cd} && {play}"], check=False)
    else:
        subprocess.run(play, shell=True, cwd=BASE, check=False)
    print(f"\nlook at survey/playtest/{a.tag}_02.png -- "
          "「아。」 + Ａ・Ｂ means this half is clean")


if __name__ == "__main__":
    main()
