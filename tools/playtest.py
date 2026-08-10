#!/usr/bin/env python3
"""Drive a cold boot from a script instead of one MCP round trip per button.

Why this exists: verifying a build meant ~35 separate emulator calls, and each
one is a full agent round trip. That cost dominated session 27's bisection --
more time went into pressing A than into building. This owns its own emulator
(the MCP server picks a free port, so it does not disturb a session that already
has one on 47800) and runs a whole boot-to-scene sequence in one shot.

    python3 tools/playtest.py --rom /mnt/c/.../PPKP9_test.nds --scene choice
    python3 tools/playtest.py --rom ... --steps "a,a,a|down|a|start" --shots all

Run it from WSL: the emucap binary and its paths are Linux-side, and `launch`
only accepts /mnt/c/... paths.

Note it can also `touch`, which the agent's own tool cannot -- that tool declares
x/y untyped, so the client sends them as strings and the server rejects them.
Here the JSON is ours, so coordinates work.
"""
import argparse, base64, json, os, subprocess, sys, time

EMUCAP = "/root/emucap/target/release/emucap-mcp"


class Session:
    def __init__(self):
        self.p = subprocess.Popen([EMUCAP], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                  bufsize=1, text=True)
        self._id = 0
        self.pids = []
        self.port = None
        self._rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                 "clientInfo": {"name": "playtest", "version": "1"}})
        self._rpc("notifications/initialized", notify=True)

    def _rpc(self, method, params=None, timeout=180, notify=False):
        self._id += 1
        mid = self._id
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        if not notify:
            msg["id"] = mid
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()
        if notify:
            return None
        dl = time.time() + timeout
        while time.time() < dl:
            line = self.p.stdout.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if obj.get("id") == mid:
                return obj
        return {"error": "timeout"}

    def call(self, name, args=None, timeout=180):
        r = self._rpc("tools/call", {"name": name, "arguments": args or {}}, timeout)
        res = r.get("result", {}) if isinstance(r, dict) else {}
        texts = [c.get("text", "") for c in res.get("content", []) if c.get("type") == "text"]
        out = {"text": "\n".join(texts)}
        try:
            out["json"] = json.loads(out["text"])
        except ValueError:
            out["json"] = None
        return out

    def sweep_stale(self):
        """Kill a previous run's emulator still holding our port.

        The SIGTERM handler cannot be relied on: when a run is cancelled while
        blocked reading the server's stdout the handler does not get to run, the
        emulator survives, and the *next* launch fails with the port taken.
        Sweeping at startup makes that self-healing. Only our own port's
        pidfiles -- never a name-based kill, which would hit another session.
        """
        d = f"/root/.local/share/emucap/desmume-nds/{self.port}"
        for name in ("bridge.pid", "desmume.pid"):
            try:
                pid = int(open(f"{d}/{name}").read().strip())
                os.kill(pid, 15)
                print(f"  swept stale {name} pid {pid} on port {self.port}", flush=True)
            except (OSError, ValueError):
                pass

    def launch(self, rom):
        b = self.call("bootstrap", {}, 60)
        self.port = (b["json"] or {}).get("listening_port")
        if self.port:
            self.sweep_stale()
            time.sleep(1.5)
        r = self.call("launch", {"content_path": rom, "system": "nds",
                                 "name": "playtest", "replace": True}, 180)
        j = r["json"] or {}
        self.port = j.get("port") or self.port
        for k in ("pid", "desmume_pid", "bridge_pid"):
            if j.get(k):
                self.pids.append(j[k])
        if not j.get("launched"):
            sys.exit(f"launch failed: {r['text'][:400]}")
        return j

    def shot(self, path):
        self.call("screenshot", {"save_path": path}, 90)
        return os.path.getsize(path) if os.path.exists(path) else 0

    def wait_for_boot(self, secs):
        """Let the game reach the title before any input.

        A plain sleep on purpose. The first attempt polled the framebuffer and
        stopped when two samples matched -- but a screenshot taken without a
        save_path returns no text, so every sample hashed the same and it
        returned after a second, straight into the BIOS animation. Every button
        of the run was then swallowed and the script sat on the title.
        """
        time.sleep(secs)

    def close(self):
        # Only ever our own pids -- a broad pkill would take out another
        # session's emulator on a different port. Also sweep the pidfiles for
        # OUR port: a run killed by a timeout never reaches this, and the
        # orphan then owns the port and the next launch fails.
        if self.port:
            d = f"/root/.local/share/emucap/desmume-nds/{self.port}"
            for name in ("bridge.pid", "desmume.pid"):
                try:
                    self.pids.append(int(open(f"{d}/{name}").read().strip()))
                except (OSError, ValueError):
                    pass
        for pid in set(self.pids):
            try:
                os.kill(pid, 15)
            except OSError:
                pass
        try:
            self.p.terminate()
        except OSError:
            pass


# Cold boot -> the A/B choice screen that session 27's regression shows up on.
# `?` marks a step whose count drifts between builds (the 守備 default moves),
# so the runner screenshots there and the caller can see where it landed.
SCENES = {
    # Cold boot -> the A/B choice screen the session-27 regression shows on.
    # `spin:N` advances N*25 frames; a press landing mid-transition is ignored.
    #
    # Character creation has a VARIABLE number of screens: 打法 is skipped when
    # the position is a pitcher, so a fixed A count stalls on some runs and
    # overshoots on others. So: press A generously (extra presses just accept a
    # default and move on) and commit the two screens that matter -- the kana
    # grid and the option sheet -- by tapping their buttons instead.
    # ★ Session 29: driven by hand end to end, and EVERY screen took A. The
    # touches this sequence used to depend on were the reason it kept desyncing
    # -- MCP `touch` is unusable from the agent side, so the coordinates could
    # never be checked interactively and were being guessed. Two claims in the
    # old comments here were simply wrong:
    #   - 「カラーは?」 is NOT touch-only. A advances it. (Run c7's fifteen dead
    #     presses were a stall with some other cause; the missing highlight is
    #     not the tell it was taken for.)
    #   - The name screen does NOT need a touch for OK. `up` then `left` x9
    #     clamps on OK from any column, because the row stops at its left edge.
    # Result: a pure-button sequence with no coordinates in it at all.
    "creation": (
        "start|spin:6"                       # title (「画面をタッチ!」) -- start works
        "|a|spin:6"                          # mode -> サクセス
        "|a|spin:8"                          # scenario -> ナイスガイ
        "|a|spin:8"                          # title card -> name entry
        "|a|spin:3"                          # type one kana (あ)
        # `up` lands DIRECTLY on OK -- confirmed by hand on two different builds
        # (survey/playtest/n05.png). The `left` x9 this line used to carry was
        # the whole bug: moving the cursor onto a mode button activates it with
        # no A pressed (landing on カナ flips the grid to katakana), so walking
        # left across 変換 converted the typed kana and the name came out
        # 「亜亜亜亜亜亜」, the name was never committed, and every later A press
        # typed into the grid instead of advancing a screen. That is what run
        # `mte0` stalled on, and almost certainly what ctl/c1-c8 stalled on too.
        "|up|spin:2"                         # cursor is now on OK
        "|a|spin:6"                          # commit the name
        "|a|spin:6"                          # past the second name field
        # 守備 -> 投打 -> 投法 -> カラー -> 変化球. 打法 is skipped for a pitcher
        # and the first option is always the default, so plain A walks all of
        # them; spare presses land on the option sheet, which A also accepts.
        + "|a|spin:5" * 5 +
        "|a|spin:6"                          # option sheet: A presses OK
        "|a|spin:16"                         # 「この設定で…」 はい
        "|start|spin:10|start|spin:20"       # disclaimer, then skip the intro
    ),
    "day1": "@creation|shot",
    # How many X it takes to reach the A/B prompt is not fixed -- the opening
    # differs with the character the game rolls -- so shoot after every one and
    # read off the run instead of betting on a count.
    "choice": "@creation|shot" + "|x|spin:4|shot" * 20,
    # ★ The way to get DEEP into a run. X toggles auto-advance so dialogue plays
    # during the spins instead of costing one A per box, but auto-advance stops
    # dead at a prompt -- the A/B choice ate a whole 150-step X run without moving
    # one frame past it. So alternate: let the spin carry the dialogue, then press
    # A, which advances a box AND answers a prompt. X is re-pressed periodically
    # because leaving a menu turns auto-advance back off.
    # Use `@skiprun` for boot tests instead of a wall of `a|spin:n`.
    "skiprun": ("x|spin:6" + "|a|spin:6|x|spin:6|a|spin:6|shot" * 30),
}


def run(sess, steps, outdir, tag, shots, gap):
    os.makedirs(outdir, exist_ok=True)
    n = 0
    for group in steps.split("|"):
        group = group.strip()
        if not group:
            continue
        if group == "shot":
            n += 1
            p = f"{outdir}/{tag}_{n:02d}.png"
            print(f"  shot -> {p} ({sess.shot(p)}B)", flush=True)
            continue
        if group.startswith("wait:"):
            time.sleep(float(group[5:]))
            continue
        if group.startswith("save:"):
            # Park the run so the next probe starts here instead of replaying
            # the prefix. Same caveat as --load-state: a state is build-bound.
            sess.call("save_state", {"path": group[5:]}, 120)
            print(f"  saved state -> {group[5:]}", flush=True)
            continue
        if group.startswith("spin:"):
            # Advance game time. A wall-clock sleep does nothing: this headless
            # DeSmuME only runs while a timed input is in flight (run_frames is
            # unsupported), so 45 s of sleep left the game still on the boot
            # logos. Pressing an inert button is how you make frames go by.
            for _ in range(int(group[5:])):
                sess.call("press_buttons", {"buttons": ["select"], "frames": 25}, 60)
            print(f"  spun {group[5:]}x25 frames", flush=True)
            continue
        if group.startswith("touch:"):
            # Bottom screen coordinates, 256x192 (the adapter README is explicit).
            # The touchscreen is sampled by the ARM7, and this adapter leaves the
            # ARM7 *frozen* by default -- so a touch is simply never read and the
            # run silently carries on pressing A into whatever screen it is on.
            # Resume both CPUs around it; we use no breakpoints, so the "racy"
            # caveat in the README does not apply here.
            x, y = (int(v) for v in group[6:].split(","))
            sess.call("resume", {"cpu": "both"}, 30)
            sess.call("touch", {"x": x, "y": y, "frames": 12})
            print(f"  touched {x},{y}", flush=True)
            continue
        for btn in group.split(","):
            btn = btn.strip()
            if not btn:
                continue
            # 25 frames: 30+ blows the emulator's 4 s input deadline.
            r = sess.call("press_buttons", {"buttons": [btn], "frames": 25}, 60)
            if r["json"] and r["json"].get("status") != "completed":
                print(f"  ! {btn}: {r['text'][:120]}", flush=True)
            # The game ignores input while a screen is transitioning. Driving
            # by hand this gap came free from the round trip; back-to-back the
            # presses land mid-wipe and vanish, which is why the first scripted
            # run "pressed" twenty buttons and never left the title.
            time.sleep(gap)
        print(f"  pressed {group}", flush=True)
        if shots == "all":
            n += 1
            p = f"{outdir}/{tag}_{n:02d}.png"
            sess.shot(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", required=True, help="/mnt/c/... path to the .nds")
    ap.add_argument("--scene", choices=sorted(SCENES))
    ap.add_argument("--steps", help="groups separated by | ; 'shot' captures")
    ap.add_argument("--out", default="/mnt/c/Users/jngji/Desktop/실험실/rom/DS/파워프로군 포켓9/ppkp9-kr/survey/playtest")
    ap.add_argument("--tag", default="run")
    ap.add_argument("--shots", choices=("marked", "all"), default="marked")
    ap.add_argument("--gap", type=float, default=0.8,
                    help="pause after each press so transitions can finish")
    ap.add_argument("--boot-wait", type=float, default=140,
                    help="inert presses used to advance the game to the title")
    ap.add_argument("--load-state",
                    help="restore this .dss instead of booting (skips the ~6 min "
                         "spin to the title AND character creation). A state "
                         "carries the whole of RAM, so the script it replays is "
                         "the one from the build it was taken on -- fine for "
                         "working out how a screen is driven, NOT for comparing "
                         "builds. For that, boot cold or continue from the .dsv.")
    a = ap.parse_args()
    steps = a.steps or SCENES[a.scene or "choice"]
    while "@" in steps:                      # @name splices another scene in
        i = steps.index("@")
        j = len(steps)
        for k in range(i + 1, len(steps)):
            if not (steps[k].isalnum() or steps[k] == "_"):
                j = k
                break
        steps = steps[:i] + SCENES[steps[i + 1:j]] + steps[j:]

    s = Session()
    import signal
    signal.signal(signal.SIGTERM, lambda *_: (s.close(), sys.exit(143)))
    try:
        j = s.launch(a.rom)
        print(f"launched pid={j.get('pid')} port={j.get('port')}", flush=True)
        # `launch` returns once the emulator is *reachable*, not once the game
        # has booted. Firing A into the BIOS/boot animation loses every press --
        # the first run of this script sat on the title screen having "pressed"
        # twenty buttons.
        if a.load_state:
            s.call("load_state", {"path": a.load_state}, 120)
            s.call("resume", {"cpu": "both"}, 30)
            print(f"restored {a.load_state}", flush=True)
        else:
            run(s, f"spin:{int(a.boot_wait)}", a.out, a.tag + "_boot", "marked", a.gap)
            # Wake the ARM7 once the boot spin is done. press_buttons auto-resumes
            # the ARM9 only, so after a cold boot the ARM7 -- which samples the
            # touchscreen -- is still frozen and every touch is silently dropped.
            # ctl3 sat on the name screen with an empty field for 50 shots
            # because of this; the same touches worked fine after --load-state,
            # where the explicit resume below already ran.
            s.call("resume", {"cpu": "both"}, 30)
        run(s, steps, a.out, a.tag, a.shots, a.gap)
    finally:
        s.close()
    print("done")


if __name__ == "__main__":
    main()
