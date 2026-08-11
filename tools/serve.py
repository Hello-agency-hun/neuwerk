#!/usr/bin/env python3
"""Fejlesztői HTTP szerver a helyi előnézethez.

Csak megnézésre való -- a leszállított csomagnak szerver NÉLKÜL is
működnie kell, ezt a tools/make_zip.py utáni kicsomagolós teszt
ellenőrzi. Ez a szkript nem része a leszállításnak.

A portot a PORT környezeti változóból veszi, hogy ne ütközzön más,
már futó szolgáltatással.
"""
import functools
import http.server
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8000"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Fejlesztés közben a cache csak félrevezet: a CSS-módosítás
        # nem látszana azonnal.
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, fmt, *args):
        # A 404-eket látni akarjuk, a 200-akat nem -- így a konzol
        # használható marad.
        if args and str(args[1]).startswith(("4", "5")):
            super().log_message(fmt, *args)


def main():
    # ThreadingHTTPServer KELL, nem sima TCPServer. Egyszálon a 2,5 MB-os
    # hero videó blokkolja az összes többi kérést, és az oldal CSS nélkül,
    # félig betöltve áll -- pont ezt mértem az első próbánál.
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"serve: http://127.0.0.1:{PORT}/  ({ROOT})")
        sys.stdout.flush()
        httpd.serve_forever()


if __name__ == "__main__":
    main()
