#!/usr/bin/env python3
"""Package the Korean patch for distribution.

Ships a PATCH, never a ROM. The player supplies their own copy of the Japanese
cartridge dump and applies the delta to it, which is how every NDS fan
translation is distributed -- handing out a patched commercial ROM would be
redistributing the game itself.

The format is xdelta3. IPS cannot be used here at all: its offsets are 24-bit,
so it tops out at 16 MB and this ROM is 64 MB.

Every release is round-tripped before it is written out: the patch is applied to
a pristine copy of the source and the result must hash to the same SHA-1 as the
build. A patch that does not reproduce the tested bytes is not a release.

    python tools/make_release.py --version 0.9
    python tools/make_release.py --version 0.9 --out D:/somewhere
"""
import argparse, hashlib, os, shutil, subprocess, sys, zlib

BASE = r"C:/Users/jngji/Desktop/실험실"
SRC = BASE + r"/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
TGT = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/builds/PPKP9_kr.nds"
RELDIR = BASE + r"/rom/DS/파워프로군 포켓9/ppkp9-kr/release"

# The one dump this patch is built against. Anything else will produce a broken
# ROM even if the patch "applies", so it is checked and printed for the user.
SRC_SHA1 = "9d37ea0bbd71bda9db9bd641460061b0ce9e3aeb"


def win2wsl(p):
    p = p.replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:] if len(p) > 2 and p[1] == ":" else p


def wsl(cmd, **kw):
    return subprocess.run(["wsl", "-e", "bash", "-lc", cmd],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def digest(path):
    h1, crc = hashlib.sha1(), 0
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h1.update(chunk)
            crc = zlib.crc32(chunk, crc)
    return h1.hexdigest(), f"{crc & 0xFFFFFFFF:08X}", os.path.getsize(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--target", default=TGT)
    ap.add_argument("--out", default=RELDIR)
    a = ap.parse_args()

    for p in (a.src, a.target):
        if not os.path.exists(p):
            sys.exit(f"없음: {p}")

    s_sha, s_crc, s_len = digest(a.src)
    t_sha, t_crc, t_len = digest(a.target)
    print(f"원본   {s_len:,}B  SHA1 {s_sha}  CRC32 {s_crc}")
    print(f"패치본 {t_len:,}B  SHA1 {t_sha}  CRC32 {t_crc}")
    if s_sha != SRC_SHA1:
        sys.exit(f"원본 SHA1이 기대값과 다르다 (기대 {SRC_SHA1}).\n"
                 f"다른 덤프로 패치를 만들면 받는 사람 쪽에서 맞지 않는다.")

    name = f"PPKP9-KR-{a.version}"
    out = os.path.join(a.out, name)
    os.makedirs(out, exist_ok=True)
    xd = os.path.join(out, f"{name}.xdelta")

    r = wsl(f"xdelta3 -e -9 -f -s '{win2wsl(a.src)}' '{win2wsl(a.target)}' "
            f"'{win2wsl(xd)}'")
    if r.returncode:
        sys.exit("xdelta3 실패:\n" + (r.stderr or r.stdout)[-1500:])
    print(f"\n패치 생성: {xd}  ({os.path.getsize(xd):,}B)")

    # ---- round trip ----
    # Apply to a COPY of the pristine source and demand the exact build hash.
    tmp = os.path.join(out, "_roundtrip.nds")
    r = wsl(f"xdelta3 -d -f -s '{win2wsl(a.src)}' '{win2wsl(xd)}' "
            f"'{win2wsl(tmp)}'")
    if r.returncode:
        sys.exit("역적용 실패:\n" + (r.stderr or r.stdout)[-1500:])
    rt_sha = digest(tmp)[0]
    os.remove(tmp)
    if rt_sha != t_sha:
        sys.exit(f"⛔ 역적용 결과가 빌드와 다르다\n  기대 {t_sha}\n  실제 {rt_sha}")
    print(f"역적용 검증 통과: {rt_sha}")

    with open(os.path.join(out, "checksums.txt"), "w", encoding="utf-8",
              newline="\r\n") as f:
        f.write(f"[적용 대상 원본 ROM]\n"
                f"  파일 크기 : {s_len:,} bytes\n"
                f"  SHA-1     : {s_sha}\n"
                f"  CRC32     : {s_crc}\n\n"
                f"[적용 후 결과]\n"
                f"  파일 크기 : {t_len:,} bytes\n"
                f"  SHA-1     : {t_sha}\n"
                f"  CRC32     : {t_crc}\n")
    print(f"체크섬 기록: {out}/checksums.txt")
    return out, s_sha, s_crc, t_sha, t_crc, os.path.getsize(xd)


if __name__ == "__main__":
    main()
