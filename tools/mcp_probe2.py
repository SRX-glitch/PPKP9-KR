#!/usr/bin/env python3
"""Corrected probe: reconnect (or launch), advance past boot, read main RAM at
offset 0, capture a real screenshot PNG. Handles MCP image content."""
import subprocess, json, sys, time, base64

EMUCAP = "/root/emucap/target/release/emucap-mcp"
ROM = "/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds"
OUT = "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/nds_boot.png"

proc = subprocess.Popen([EMUCAP], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, bufsize=1, text=True)
_id = 0
def rpc(method, params=None, timeout=60, notify=False):
    global _id
    msg = {"jsonrpc":"2.0","method":method}
    if params is not None: msg["params"]=params
    if not notify: _id+=1; msg["id"]=_id
    proc.stdin.write(json.dumps(msg)+"\n"); proc.stdin.flush()
    if notify: return None
    deadline=time.time()+timeout
    while time.time()<deadline:
        line=proc.stdout.readline()
        if not line: break
        line=line.strip()
        if not line: continue
        try: obj=json.loads(line)
        except: continue
        if obj.get("id")==_id: return obj
    return {"error":"timeout"}
def call(name,args=None,timeout=60):
    r=rpc("tools/call",{"name":name,"arguments":args or {}},timeout=timeout)
    res=r.get("result",{})
    content=res.get("content",[])
    texts=[c.get("text","") for c in content if c.get("type")=="text"]
    images=[c.get("data","") for c in content if c.get("type")=="image"]
    return {"text":"\n".join(texts), "image":images[0] if images else None, "raw":res}

rpc("initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe2","version":"0"}})
rpc("notifications/initialized",notify=True)
call("bootstrap",{},30)
st=call("status",{},30)
connected=False
try: connected=json.loads(st["text"]).get("connected")
except: pass
if not connected:
    print("launching..."); print(call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)["text"][:200])
else:
    print("reattached to running desmume")

# advance past boot: resume ARM9, let it run, pause
call("resume",{},30)
time.sleep(6)
call("pause",{},30)

st=json.loads(call("status",{},30)["text"])
print("status: connected=%s state=%s frame=%s" % (st.get("connected"), st.get("state"), st.get("frame")))

# read main RAM at offset 0 (main region is 4MB, offset-addressed)
rm=call("read_memory",{"memory_type":"main","address":"0x0","length":32},30)
print("read main@0x0:", rm["text"][:200])
# also read via arm9 absolute address
rm2=call("read_memory",{"memory_type":"arm9","address":"0x02000000","length":16},30)
print("read arm9@0x02000000:", rm2["text"][:200])

# screenshot
ss=call("screenshot",{},60)
img=ss["image"]
if not img:
    # maybe base64 embedded in text json
    try: img=json.loads(ss["text"]).get("png_base64")
    except: pass
if img:
    raw=base64.b64decode(img)
    open(OUT,"wb").write(raw)
    print(f"SCREENSHOT SAVED: {len(raw)} bytes -> {OUT}")
else:
    print("screenshot text:", ss["text"][:200], "keys:", list(ss["raw"].keys()))

proc.terminate()
print("DONE")
