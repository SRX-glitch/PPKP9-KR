#!/usr/bin/env python3
"""Pull a screenshot out of the WSL emulator host and blow up the text box.

The DS bottom screen is 256x192 at y=192..384 in emucap's stacked capture; the
dialogue box sits in its upper half. Reading 12px Hangul off a 1x capture is
guesswork, so every on-screen check goes through here.
"""
import subprocess, sys, os
from PIL import Image

TMP = r"C:/Users/jngji/AppData/Local/Temp/ppkp9shots"
OUT = r"C:/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"


def fetch(name):
    os.makedirs(TMP, exist_ok=True)
    dst = f"{TMP}/{name}"
    subprocess.run(["wsl.exe", "-d", "Ubuntu-24.04", "-u", "root", "--", "cp",
                    f"/root/{name}", f"/mnt/c/Users/jngji/AppData/Local/Temp/ppkp9shots/{name}"],
                   check=True, env={**os.environ, "MSYS2_ARG_CONV_EXCL": "*"})
    return dst


def zoom(name, box=(0, 192, 256, 384), scale=4, out=None):
    src = fetch(name)
    img = Image.open(src).convert("RGB").crop(box)
    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    dst = out or os.path.join(OUT, name.replace(".png", "_zoom.png"))
    img.save(dst)
    print(dst)
    return dst


if __name__ == "__main__":
    name = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "full":
        zoom(name, box=(0, 0, 256, 384), scale=3)
    else:
        zoom(name)
