#!/usr/bin/env python3
"""Fejlesztői HTTP szerver a helyi előnézethez.

Csak megnézésre való -- a leszállított csomagnak szerver NÉLKÜL is
működnie kell, ezt a tools/make_zip.py utáni kicsomagolós teszt
ellenőrzi. Ez a szkript nem része a leszállításnak.

Két dolog, ami nem magától értetődő, és mindkettő mérésből derült ki:

1. ThreadingHTTPServer kell, nem sima TCPServer. Egyszálon a hero videó
   blokkolja az összes többi kérést, és az oldal CSS nélkül, félig
   betöltve áll.

2. HTTP Range támogatás kell. A SimpleHTTPRequestHandler NEM támogatja,
   ezért a böngésző a videót seekable: [0, 0]-ként látja, még akkor is,
   ha teljesen bepufferelte. Következmény: a Solutions szekcióban a
   video.currentTime értékadás némán hatástalan marad, és mind a négy
   képességgomb ugyanazt a képkockát mutatja. Éles szerveren (Apache,
   nginx, IIS) a Range alapból megy, de a helyi előnézetnek is hűnek
   kell lennie, különben működő kódot hiszünk hibásnak.

A portot a PORT környezeti változóból veszi, hogy ne ütközzön más,
már futó szolgáltatással.
"""
import functools
import http.server
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PORT = int(os.environ.get("PORT", "8000"))
RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Fejlesztés közben a cache csak félrevezet: a CSS-módosítás
        # nem látszana azonnal.
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def send_head(self):
        """A Range fejléc kiszolgálása. Enélkül a videó nem tekerhető."""
        rng = self.headers.get("Range")
        if not rng:
            # Range nélküli kérésnél is jelezzük, hogy tudunk Range-et --
            # e nélkül egyes böngészők meg sem próbálják.
            f = super().send_head()
            return f

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()

        m = RANGE_RE.match(rng.strip())
        if not m:
            self.send_error(400, "Invalid Range")
            return None

        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        size = os.fstat(f.fileno()).st_size
        start_s, end_s = m.group(1), m.group(2)

        if start_s == "":
            # bytes=-N  -> az utolsó N bájt
            length = int(end_s or 0)
            start = max(0, size - length)
            end = size - 1
        else:
            start = int(start_s)
            end = int(end_s) if end_s else size - 1

        if start >= size or start > end:
            f.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.end_headers()
            return None

        end = min(end, size - 1)
        f.seek(start)

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()

        self._range_remaining = end - start + 1
        return f

    def copyfile(self, source, outputfile):
        remaining = getattr(self, "_range_remaining", None)
        if remaining is None:
            return super().copyfile(source, outputfile)
        self._range_remaining = None
        while remaining > 0:
            chunk = source.read(min(64 * 1024, remaining))
            if not chunk:
                break
            outputfile.write(chunk)
            remaining -= len(chunk)

    def log_message(self, fmt, *args):
        # A 404-eket látni akarjuk, a 200-akat nem -- így a konzol
        # használható marad.
        if args and str(args[1]).startswith(("4", "5")):
            super().log_message(fmt, *args)


def main():
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"serve: http://127.0.0.1:{PORT}/  ({ROOT})")
        sys.stdout.flush()
        httpd.serve_forever()


if __name__ == "__main__":
    main()
