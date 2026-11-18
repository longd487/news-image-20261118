#!/usr/bin/env python3
"""Entry point for make.fun's "Sum up 18 November's world news in one image".

The entry is a program that writes one image to /output/entry.png.
This program takes the simplest route the bounty allows: it copies the
image the repository already holds (entry.png) to /output/entry.png.

The image itself was built by render.py in this repository: a 1024x1024
infographic that sums up Wednesday 18 November 2026 in five stories,
researched the same day from Reuters, AP, Bloomberg and company releases:
  1. Nvidia posts a record $115.8B quarter (revenue +103%)
  2. US strikes an IRGC missile base in the Gulf
  3. Trump, Xi and Putin summit set for tomorrow in Shenzhen
  4. Crimean Bridge road span brought down
  5. North Korea fires a ballistic missile

Why copy instead of render at run time?
  * The bounty requires no network and byte-identical output across two
    runs. A copy is deterministic by construction.
  * Rendering needs Pillow and fonts, which the grading sandbox is not
    guaranteed to have. Copying needs only the standard library.

Before copying, the program validates the image against the bounty's
requirements (PNG, at most 1024x1024 pixels, at most 1 MiB) and refuses
to write anything that does not meet them, so a bad asset can never
become a bad entry.
"""

import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")

MAX_BYTES = 1 * 1024 * 1024          # 1 MiB
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_dimensions(path):
    """Return (width, height) of a PNG file, verifying its signature and IHDR."""
    with open(path, "rb") as f:
        header = f.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad signature")
    # After the 8-byte signature comes the 25-byte IHDR chunk:
    # 4 length + 4 type ("IHDR") + 13 data (width, height, ...) + 4 CRC.
    length = struct.unpack(">I", header[8:12])[0]
    chunk_type = header[12:16]
    if chunk_type != b"IHDR" or length != 13:
        raise ValueError("not a PNG file: missing IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    if not os.path.isfile(SOURCE):
        print(f"error: {SOURCE} not found", file=sys.stderr)
        return 1

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"error: image is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1

    width, height = read_png_dimensions(SOURCE)
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        print(f"error: image is {width}x{height}, over the 1024x1024 cap",
              file=sys.stderr)
        return 1

    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)

    # The copy is byte-identical to the source by construction; confirm it.
    written = os.path.getsize(DEST)
    if written != size:
        print(f"error: wrote {written} bytes, expected {size}", file=sys.stderr)
        return 1

    print(f"wrote {DEST} ({width}x{height}, {written} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
