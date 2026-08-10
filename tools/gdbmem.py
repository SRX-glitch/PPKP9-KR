#!/usr/bin/env python3
"""Bulk memory access over the DeSmuME fork's GDB remote stub.

Why: the emucap MCP `dump_memory` times out on this adapter and `read_memory`
moves only ~8KB per round trip, so a 4MB RAM image is ~512 MCP calls.  The
stub speaks plain gdb-remote, so a local socket loop pulls the same image in
seconds.  Read-only use here -- the MCP session stays the owner of execution
control (run/pause/breakpoints).

The emucap bridge normally holds the stub connection, so this only works when
the stub accepts a second client; probe first with --ping.

Usage:
    python3 gdbmem.py --ping [--port N]
    python3 gdbmem.py --dump 0x02000000 0x400000 out.bin [--port N]
"""
import socket, sys

DEFAULT_PORT = 40895


class Gdb:
    def __init__(self, port=DEFAULT_PORT, host="127.0.0.1", timeout=5.0):
        self.s = socket.create_connection((host, port), timeout)
        self.s.settimeout(timeout)
        self.buf = b""

    def _send(self, payload):
        cks = sum(payload.encode()) & 0xFF
        self.s.sendall(b"$" + payload.encode() + b"#" + f"{cks:02x}".encode())

    def _recv(self):
        while True:
            i = self.buf.find(b"#")
            if i >= 0 and len(self.buf) >= i + 3:
                start = self.buf.find(b"$")
                pkt = self.buf[start + 1:i]
                self.buf = self.buf[i + 3:]
                self.s.sendall(b"+")
                return pkt
            more = self.s.recv(65536)
            if not more:
                raise EOFError("stub closed")
            self.buf += more.replace(b"+", b"", 1) if self.buf == b"" and more.startswith(b"+") else more

    def cmd(self, payload):
        self._send(payload)
        return self._recv()

    def read(self, addr, length, chunk=0x400):
        out = bytearray()
        while length > 0:
            n = min(chunk, length)
            r = self.cmd(f"m{addr:x},{n:x}")
            if r.startswith(b"E") or len(r) != n * 2:
                raise RuntimeError(f"read failed @0x{addr:08x}: {r[:32]!r}")
            out += bytes.fromhex(r.decode())
            addr += n
            length -= n
        return bytes(out)

    def close(self):
        self.s.close()


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else DEFAULT_PORT
    if "--ping" in sys.argv:
        g = Gdb(port)
        print("connected; ? ->", g.cmd("?"))
        print("first 16B @0x02000000:", g.read(0x02000000, 16).hex())
        g.close()
    elif "--dump" in sys.argv:
        i = sys.argv.index("--dump")
        addr = int(sys.argv[i + 1], 0)
        length = int(sys.argv[i + 2], 0)
        out = sys.argv[i + 3]
        g = Gdb(port)
        data = g.read(addr, length)
        open(out, "wb").write(data)
        print(f"wrote {out} {len(data)} bytes from 0x{addr:08x}")
        g.close()
