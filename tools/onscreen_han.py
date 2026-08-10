import sys, subprocess, os, shutil, time
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
ROM="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/Power Pro Kun Pocket 9 (Japan).nds"
from fontenc import encode_glyph
from PIL import Image, ImageFont, ImageDraw
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
def bitmap(cp,sz=12,oy=-3,W=12,H=8,thr=90):
    f=ImageFont.truetype("/mnt/c/Windows/Fonts/malgun.ttf",sz)
    img=Image.new("L",(W,H),0); d=ImageDraw.Draw(img); d.text((0,oy),chr(cp),fill=255,font=f)
    px=img.load(); return [[1 if px[c,r]>thr else 0 for c in range(W)] for r in range(H)]
try:
    from emucap_drv import Emucap
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.4); e.call("pause",{},30)
    # alternate 한/글 across glyphs so name shows 한글한글
    han=encode_glyph(bitmap(0xD55C)); geul=encode_glyph(bitmap(0xAE00))
    region=0x0207E000; length=0x8000
    buf=bytearray()
    i=0
    while len(buf)<length:
        buf+= han if (i%2==0) else geul; i+=1
    buf=bytes(buf[:length])
    for off in range(0,length,0x2000):
        e.call("write_memory",{"memory_type":"arm9","address":hex(region+off),"hex":buf[off:off+0x2000].hex()},40)
    e.call("resume",{},20); time.sleep(0.5); e.call("pause",{},20)
    e.screenshot(f"{SD}/onscreen_han.png")
    log("shot saved")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
