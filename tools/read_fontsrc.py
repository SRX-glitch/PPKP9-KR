import sys, json, subprocess, os, shutil, time, zlib, struct
sys.path.insert(0,"/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/tools")
shutil.rmtree("/root/.local/share/emucap/desmume-nds", ignore_errors=True)
SD="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"
LOG=open("/root/probe.log","w",encoding="utf-8")
def log(*a): print(*a, file=LOG, flush=True)
def png_gray(path,w,h,pix):
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    raw=bytearray()
    for y in range(h): raw.append(0); raw+=pix[y*w:(y+1)*w]
    open(path,"wb").write(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,0,0,0,0))+ch(b"IDAT",zlib.compress(bytes(raw),9))+ch(b"IEND",b""))
def tiles_4bpp(data,per_row=32):
    n=len(data)//32; rows=(n+per_row-1)//per_row; W=per_row*8; H=rows*8; pix=bytearray(W*H)
    for t in range(n):
        tx=(t%per_row)*8; ty=(t//per_row)*8
        for by in range(8):
            for bx in range(4):
                b=data[t*32+by*4+bx]
                pix[(ty+by)*W+tx+bx*2]=(b&0xF)*17; pix[(ty+by)*W+tx+bx*2+1]=((b>>4)&0xF)*17
    return W,H,pix
try:
    from emucap_drv import Emucap, ROM
    e=Emucap()
    e.call("bootstrap",{},30)
    if not (e.call("status",{},30)["json"] or {}).get("connected"):
        e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},180)
    e.call("load_state",{"path":"/root/ppkp9_kbd.dss"},30)
    e.call("resume",{},30); time.sleep(0.6); e.call("pause",{},30)
    def rd(addr,length,mt="main"):
        out=bytearray(); a=addr
        while length>0:
            n=min(0x1000,length)
            j=e.call("read_memory",{"memory_type":mt,"address":hex(a),"length":n},60)["json"]
            if not j or "hex" not in j: break
            out+=bytes.fromhex(j["hex"]); a+=n; length-=n
        return bytes(out)
    # DMA3 SAD was 0x022D3720. main memory_type offset0=0x02000000, so main offset=0x2D3720
    base=0x2D0000; ln=0x40000
    buf=rd(base,ln,"main")
    open(f"{SD}/fontsrc.bin","wb").write(buf)
    log(f"read main 0x{0x02000000+base:08x} len {len(buf)}")
    # compare with known VRAM font kbd_subBG[0x8000:0xC000]
    vram=open(f"{SD}/kbd_subBG.bin","rb").read()
    fref=vram[0x8000:0xC000]  # 16KB
    # search fontsrc for the first 64 nonzero-distinctive bytes of fref
    # find a distinctive 32B tile in fref
    import binascii
    hits=[]
    # take several 32B needles from fref that are non-blank
    needles=[]
    for o in range(0,len(fref)-32,32):
        t=fref[o:o+32]
        if 40<sum(bin(x).count("1") for x in t)<180 and len(set(t))>6:
            needles.append((o,t))
        if len(needles)>=8: break
    for o,t in needles:
        idx=buf.find(t)
        log(f"  needle vram@0x{0x8000+o:x}: {'FOUND at fontsrc+0x%x (abs 0x%08x)'%(idx,0x02000000+base+idx) if idx>=0 else 'not found'}")
    # render the region around SAD offset
    sad_off=0x2D3720-base
    seg=buf[sad_off: sad_off+0x4000]
    W,H,pix=tiles_4bpp(seg); png_gray(f"{SD}/fontsrc_at_sad.png",W,H,pix)
    log(f"rendered fontsrc_at_sad.png from abs 0x022D3720")
    e.close(); log("DONE")
except Exception:
    import traceback; log("ERR", traceback.format_exc())
finally:
    LOG.close()
    subprocess.run(["pkill","-9","-f","[d]esmume-cli"])
    subprocess.run(["pkill","-9","-f","[e]mucap-desmume-nds-bridge"])
    os._exit(0)
