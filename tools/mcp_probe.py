#!/usr/bin/env python3
"""Minimal MCP stdio client to drive emucap-mcp (WSL) and verify the NDS stack:
initialize -> bootstrap -> launch(rom, nds) -> status -> read_memory + screenshot."""
import subprocess, json, sys, threading, time, base64, os

EMUCAP = "/root/emucap/target/release/emucap-mcp"
ROM = sys.argv[1] if len(sys.argv) > 1 else "/mnt/c/Users/jngji/Desktop/실험실/rom/Power Pro Kun Pocket 9 (Japan).nds"

proc = subprocess.Popen([EMUCAP], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, bufsize=1, text=True)
_id = 0
def rpc(method, params=None, timeout=60, notify=False):
    global _id
    msg = {"jsonrpc": "2.0", "method": method}
    if params is not None: msg["params"] = params
    if not notify:
        _id += 1; msg["id"] = _id
    proc.stdin.write(json.dumps(msg) + "\n"); proc.stdin.flush()
    if notify: return None
    deadline = time.time() + timeout
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line: break
        line = line.strip()
        if not line: continue
        try: obj = json.loads(line)
        except: continue
        if obj.get("id") == _id:
            return obj
    return {"error": "timeout"}

def call_tool(name, args=None, timeout=60):
    r = rpc("tools/call", {"name": name, "arguments": args or {}}, timeout=timeout)
    # unwrap MCP tool result content
    if "result" in r:
        c = r["result"].get("content", [])
        texts = [x.get("text","") for x in c if x.get("type")=="text"]
        return "\n".join(texts) if texts else json.dumps(r["result"])[:400]
    return json.dumps(r)[:400]

print("== initialize ==")
init = rpc("initialize", {"protocolVersion":"2024-11-05","capabilities":{},
                          "clientInfo":{"name":"probe","version":"0"}})
print("  server:", init.get("result",{}).get("serverInfo",{}))
rpc("notifications/initialized", notify=True)

print("== bootstrap ==")
b = call_tool("bootstrap", {}, timeout=30)
try:
    bj = json.loads(b); print("  listening_port:", bj.get("listening_port"), "ok:", bj.get("ok"))
except: print("  ", b[:200])

print("== launch (nds, headless) ==")
lr = call_tool("launch", {"content_path": ROM, "system": "nds", "name": "ppkp9"}, timeout=120)
print("  ", lr[:500])

print("== status ==")
st = call_tool("status", {}, timeout=30)
try:
    sj = json.loads(st)
    print("  connected:", sj.get("connected"), "state:", sj.get("state"),
          "system:", sj.get("system") or sj.get("backend"))
    mt = sj.get("memory_types"); print("  memory_types:", mt)
except:
    print("  ", st[:400])

print("== resume a few frames then step ==")
print("  resume:", call_tool("resume", {}, timeout=30)[:150])
time.sleep(2)
print("  pause:", call_tool("pause", {}, timeout=30)[:150])

print("== read_memory main RAM 0x02000000 (32 bytes) ==")
rm = call_tool("read_memory", {"memory_type":"main","address":"0x02000000","length":32}, timeout=30)
print("  ", rm[:300])

print("== screenshot ==")
ss = call_tool("screenshot", {}, timeout=60)
try:
    sj = json.loads(ss)
    p = sj.get("png_base64") or sj.get("data") or ""
    if p:
        raw = base64.b64decode(p)
        out = "/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/nds_boot.png"
        open(out,"wb").write(raw)
        print(f"  screenshot OK: {len(raw)} bytes -> {out} ({sj.get('width')}x{sj.get('height')})")
    else:
        print("  screenshot payload keys:", list(sj.keys()))
except Exception as e:
    print("  screenshot raw:", ss[:300], "err:", e)

proc.terminate()
print("DONE")
