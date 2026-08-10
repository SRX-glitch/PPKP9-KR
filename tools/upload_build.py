#!/usr/bin/env python3
"""Upload a build to GitHub as a Release — as an xdelta PATCH, never the ROM.

Ships the same artifact policy as make_release.py: the .nds itself is a
commercial ROM and never leaves this machine. What goes up is the round-trip
verified delta against the one known-good Japanese dump, plus checksums, so
the exact build can be reproduced anywhere the original cartridge dump exists.

    python tools/upload_build.py                          # newest builds/*.nds
    python tools/upload_build.py --build builds/PPKP9_kr_v202.nds
    python tools/upload_build.py --build ... --notes "프롤로그 전환 수정"

Tag/title are derived from the filename (PPKP9_kr_v202.nds -> build-v202).
Re-running for the same tag overwrites that release's assets (--clobber).
"""
import argparse, glob, os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_release as mr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "SRX-glitch/PPKP9-KR"
OUTDIR = os.path.join(ROOT, "release", "_gh")  # gitignored staging area


def find_gh():
    gh = shutil.which("gh")
    if gh:
        return gh
    for p in (r"C:\Program Files\GitHub CLI\gh.exe",
              r"C:\Program Files (x86)\GitHub CLI\gh.exe"):
        if os.path.exists(p):
            return p
    sys.exit("gh CLI를 찾을 수 없다 — 설치 후 다시 실행")


def newest_build():
    nds = glob.glob(os.path.join(ROOT, "builds", "*.nds"))
    if not nds:
        sys.exit("builds/에 .nds가 없다")
    return max(nds, key=os.path.getmtime)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", help="빌드 .nds 경로 (생략 시 builds/ 최신)")
    ap.add_argument("--tag", help="릴리스 태그 (생략 시 파일명에서 유도)")
    ap.add_argument("--notes", default="", help="릴리스 노트 본문")
    a = ap.parse_args()

    build = os.path.abspath(a.build) if a.build else newest_build()
    if not os.path.exists(build):
        sys.exit(f"없음: {build}")
    stem = os.path.splitext(os.path.basename(build))[0]

    if a.tag:
        tag = a.tag
    else:
        m = re.search(r"_v(\w+)$", stem) or re.search(r"v(\w+)", stem)
        if not m:
            sys.exit(f"파일명에서 버전을 못 찾았다({stem}) — --tag로 지정")
        tag = f"build-v{m.group(1)}"

    # ---- source-dump check + delta + round trip (make_release helpers) ----
    if not os.path.exists(mr.SRC):
        sys.exit(f"원본 ROM 없음: {mr.SRC}")
    s_sha, s_crc, s_len = mr.digest(mr.SRC)
    if s_sha != mr.SRC_SHA1:
        sys.exit(f"원본 SHA1이 기대값과 다르다 (기대 {mr.SRC_SHA1})")
    t_sha, t_crc, t_len = mr.digest(build)
    print(f"빌드 {os.path.basename(build)}  SHA1 {t_sha}  CRC32 {t_crc}")

    out = os.path.join(OUTDIR, tag)
    os.makedirs(out, exist_ok=True)
    xd = os.path.join(out, f"{stem}.xdelta")

    r = mr.wsl(f"xdelta3 -e -9 -f -s '{mr.win2wsl(mr.SRC)}' "
               f"'{mr.win2wsl(build)}' '{mr.win2wsl(xd)}'")
    if r.returncode:
        sys.exit("xdelta3 실패:\n" + (r.stderr or r.stdout)[-1500:])

    tmp = os.path.join(out, "_roundtrip.nds")
    r = mr.wsl(f"xdelta3 -d -f -s '{mr.win2wsl(mr.SRC)}' '{mr.win2wsl(xd)}' "
               f"'{mr.win2wsl(tmp)}'")
    if r.returncode:
        sys.exit("역적용 실패:\n" + (r.stderr or r.stdout)[-1500:])
    rt_sha = mr.digest(tmp)[0]
    os.remove(tmp)
    if rt_sha != t_sha:
        sys.exit(f"⛔ 역적용 결과가 빌드와 다르다\n  기대 {t_sha}\n  실제 {rt_sha}")
    print(f"패치 생성·역적용 검증 통과 ({os.path.getsize(xd):,}B)")

    ck = os.path.join(out, "checksums.txt")
    with open(ck, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(f"[적용 대상 원본 ROM]\n  파일 크기 : {s_len:,} bytes\n"
                f"  SHA-1     : {s_sha}\n  CRC32     : {s_crc}\n\n"
                f"[적용 후 결과 = {os.path.basename(build)}]\n"
                f"  파일 크기 : {t_len:,} bytes\n"
                f"  SHA-1     : {t_sha}\n  CRC32     : {t_crc}\n")

    # ---- GitHub Release ----
    gh = find_gh()
    title = stem.replace("_", " ")
    notes = a.notes or f"자동 업로드: {os.path.basename(build)}\n\nSHA-1 {t_sha}"
    exists = subprocess.run([gh, "release", "view", tag, "-R", REPO],
                            capture_output=True).returncode == 0
    if exists:
        cmd = [gh, "release", "upload", tag, xd, ck, "--clobber", "-R", REPO]
    else:
        cmd = [gh, "release", "create", tag, xd, ck,
               "-t", title, "-n", notes, "-R", REPO]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit("gh 실패:\n" + (r.stderr or r.stdout)[-1500:])
    print(f"업로드 완료: https://github.com/{REPO}/releases/tag/{tag}")

    # ---- 'latest' 릴리스: ROM 본체를 고정 이름으로 교체 업로드 ----
    # 사용자 결정(2026-08-10): 프라이빗 저장소, 외부 실기 테스트용으로 ROM
    # 자체를 올린다. 항상 같은 파일명이라 다운로드 URL이 고정된다.
    latest_rom = os.path.join(out, "PPKP9_kr_latest.nds")
    shutil.copyfile(build, latest_rom)
    lnotes = (f"현재 빌드: {os.path.basename(build)}\n"
              f"SHA-1 {t_sha}  CRC32 {t_crc}\n\n{a.notes}".rstrip())
    if subprocess.run([gh, "release", "view", "latest", "-R", REPO],
                      capture_output=True).returncode != 0:
        r = subprocess.run([gh, "release", "create", "latest",
                            "-t", f"최신 빌드 ({stem})", "-n", lnotes,
                            "-R", REPO],
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode:
            sys.exit("latest 릴리스 생성 실패:\n" + (r.stderr or r.stdout)[-1500:])
    else:
        subprocess.run([gh, "release", "edit", "latest",
                        "-t", f"최신 빌드 ({stem})", "-n", lnotes, "-R", REPO],
                       capture_output=True)
    print(f"ROM 업로드 중… ({os.path.getsize(latest_rom):,}B)")
    r = subprocess.run([gh, "release", "upload", "latest", latest_rom,
                        "--clobber", "-R", REPO],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    os.remove(latest_rom)
    if r.returncode:
        sys.exit("ROM 업로드 실패:\n" + (r.stderr or r.stdout)[-1500:])
    print(f"교체 완료: https://github.com/{REPO}/releases/download/latest/"
          f"PPKP9_kr_latest.nds  ({stem})")


if __name__ == "__main__":
    main()
