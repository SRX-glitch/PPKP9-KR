#!/usr/bin/env python3
"""Reusable emucap MCP stdio driver for the NDS ROM. Import or run standalone."""
import subprocess, json, time, base64, os

EMUCAP = "/root/emucap/target/release/emucap-mcp"
ROM = "/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds"
OUTDIR = "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey"

class Emucap:
    def __init__(self):
        self.p = subprocess.Popen([EMUCAP], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, bufsize=1, text=True)
        self._id = 0
        self._rpc("initialize", {"protocolVersion":"2024-11-05","capabilities":{},
                                 "clientInfo":{"name":"drv","version":"0"}})
        self._rpc("notifications/initialized", notify=True)
    def _rpc(self, method, params=None, timeout=120, notify=False):
        self._id += 1; mid=self._id
        msg={"jsonrpc":"2.0","method":method}
        if params is not None: msg["params"]=params
        if not notify: msg["id"]=mid
        self.p.stdin.write(json.dumps(msg)+"\n"); self.p.stdin.flush()
        if notify: return None
        dl=time.time()+timeout
        while time.time()<dl:
            line=self.p.stdout.readline()
            if not line: break
            line=line.strip()
            if not line: continue
            try: obj=json.loads(line)
            except: continue
            if obj.get("id")==mid: return obj
        return {"error":"timeout"}
    def call(self, name, args=None, timeout=120):
        r=self._rpc("tools/call", {"name":name,"arguments":args or {}}, timeout=timeout)
        res=r.get("result",{}); content=res.get("content",[])
        texts=[c.get("text","") for c in content if c.get("type")=="text"]
        images=[c.get("data","") for c in content if c.get("type")=="image"]
        out={"text":"\n".join(texts), "image":images[0] if images else None}
        try: out["json"]=json.loads(out["text"])
        except: out["json"]=None
        return out
    def screenshot(self, path):
        ss=self.call("screenshot", {}, 60)
        img=ss["image"]
        if not img and ss["json"]: img=ss["json"].get("png_base64")
        if img:
            raw=base64.b64decode(img); open(path,"wb").write(raw)
            return len(raw)
        return 0
    def close(self):
        try: self.p.terminate()
        except: pass

if __name__=="__main__":
    import sys
    e=Emucap()
    print("boot:", e.call("bootstrap",{},30)["text"][:80])
    st=e.call("status",{},30)
    if not (st["json"] or {}).get("connected"):
        print("launch:", e.call("launch",{"content_path":ROM,"system":"nds","name":"ppkp9"},120)["text"][:120])
    # drive: advance through intro, tapping start/A, capture screenshots
    seq=[]
    for i in range(10):
        e.call("resume",{},30)
        time.sleep(1.5)
        e.call("pause",{},30)
        n=e.screenshot(f"{OUTDIR}/drv_{i:02d}.png")
        st=e.call("status",{},30)
        frame=(st["json"] or {}).get("frame")
        print(f"frame~{frame} shot drv_{i:02d}.png {n}B")
        # alternate inputs to advance menus
        if i%2==0:
            e.call("press_buttons",{"buttons":["start"],"frames":4},30)
        else:
            e.call("press_buttons",{"buttons":["a"],"frames":4},30)
        # also a touch tap center-bottom (many PPP screens are touch)
        e.call("touch",{"x":128,"y":96,"frames":4},30)
    e.close()
    print("DONE")
