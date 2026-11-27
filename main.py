#!/usr/bin/env python3
"""news-26 b60 numbers entry runner (stdlib only, no PIL, no network).

Copies the pre-rendered entry.png that ships in this repository into the
directory named by MAKEFUN_OUTPUT_DIR (default "out"). The grader runs this
program with the standard library only, so it must not import PIL, numpy or
anything outside the standard library. The image itself was rendered at
build time by gen.py (Pillow) and committed to the repo as entry.png; this
file only moves bytes. It verifies the copy by comparing SHA-256 digests of
source and destination, and it refuses to run if the image is missing or
larger than the 1 MiB competition cap, so a bad bundle fails loudly here
instead of silently shipping a broken entry to the judge. The copy is
verified byte-for-byte, so a truncated write is caught here, not by the gate.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.png"
MAX_BYTES = 1048576
FALLBACK_OUTPUT_DIR = "out"


def _source_path():
    """Locate entry.png next to this file, or in the current directory."""
    here = os.path.dirname(os.path.abspath(__file__))
    first = os.path.join(here, ENTRY_NAME)
    if os.path.isfile(first):
        return first
    second = os.path.join(os.getcwd(), ENTRY_NAME)
    if os.path.isfile(second):
        return second
    raise FileNotFoundError("entry.png not found next to main.py (%s) or in cwd (%s)"
                            % (first, second))


def _output_dir():
    """Read the grader output directory from the environment, default "out"."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_OUTPUT_DIR)
    if not wanted:
        wanted = FALLBACK_OUTPUT_DIR
    return os.path.abspath(wanted)


def _sha256(path):
    """Return the hex SHA-256 digest of the file at path, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_source(path):
    """Validate the bundled image before copying: exists, PNG magic, size cap."""
    size = os.path.getsize(path)
    if size <= 0 or size > MAX_BYTES:
        raise ValueError("entry.png size %d outside 1..%d bytes" % (size, MAX_BYTES))
    with open(path, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png does not start with the PNG magic bytes "
                         "(got %r)" % magic)
    return size


def copy_entry():
    """Copy entry.png into the output dir and verify the copy byte-for-byte."""
    src = _source_path()
    size = _check_source(src)
    outdir = _output_dir()
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, ENTRY_NAME)
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != size:
        raise ValueError("copied entry.png size mismatch: %d != %d"
                         % (os.path.getsize(dst), size))
    if _sha256(dst) != _sha256(src):
        raise ValueError("copied entry.png SHA-256 mismatch")
    return dst, size, _sha256(dst)


def report(dst, size, digest):
    """Print one line per fact the operator needs: path, size, digest."""
    print("entry: %s" % dst)
    print("bytes: %d" % size)
    print("sha256: %s" % digest)
    print("ok: copied entry.png to MAKEFUN_OUTPUT_DIR")


def main(argv):
    """Entry point: copy the image, verify it, report it, exit non-zero on error."""
    if len(argv) > 1:
        print("usage: main.py (no arguments; reads MAKEFUN_OUTPUT_DIR)", file=sys.stderr)
        return 2
    try:
        dst, size, digest = copy_entry()
    except (OSError, ValueError, FileNotFoundError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    report(dst, size, digest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
